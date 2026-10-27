#!/usr/bin/env pwsh
# Commit validated automation output to one fixed branch per job, open or
# update its pull request, and merge it unless the repository variable
# AUTOMATION_AUTO_MERGE is set to "false".
#
# A fixed branch means a newer run replaces the older proposal instead of
# leaving stale pull requests that later conflict with the default branch.

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $Branch,
    [Parameter(Mandatory)] [string] $Title,
    [Parameter(Mandatory)] [string] $Body,
    [Parameter(Mandatory)] [string[]] $Paths,
    [string] $AutoMerge = $env:AUTOMATION_AUTO_MERGE
)

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$Base = $env:BASE_BRANCH
if (-not $Base) {
    throw "BASE_BRANCH is not set"
}

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git switch -C $Branch
git add -- @Paths
git commit -m $Title
git push --force origin "HEAD:refs/heads/$Branch"

$Existing = gh pr list --base $Base --head $Branch --state open --json number --jq '.[0].number'
if ($Existing) {
    gh pr edit $Existing --title $Title --body $Body
    $Number = $Existing
}
else {
    $Url = gh pr create --base $Base --head $Branch --title $Title --body $Body
    $Number = ($Url -split "/")[-1]
}

if ($AutoMerge -eq "false") {
    "Pull request #$Number is waiting for manual review." >> $env:GITHUB_STEP_SUMMARY
    return
}

# The calling workflow has already run the repository checks on exactly this
# commit. Branch protection may still refuse the merge; that leaves the pull
# request open for a person instead of failing the run.
$PSNativeCommandUseErrorActionPreference = $false
gh pr merge $Number --squash --delete-branch
if ($LASTEXITCODE -eq 0) {
    "Merged pull request #$Number automatically." >> $env:GITHUB_STEP_SUMMARY
}
else {
    Write-Warning "Could not merge pull request #$Number automatically; it stays open for review."
    "Pull request #$Number could not be merged automatically and is waiting for review." >> $env:GITHUB_STEP_SUMMARY
}
