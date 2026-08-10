# 基督宗派专题词库来源与取词原则

更新日期：2026-08-10

本文件记录 `catholicism_expansion_2026.txt` 与 `christian_traditions_2026.txt`
的核对来源，覆盖天主教、新教、东正教、东方正统教会和东方亚述教会。
词库只采用经人工核对的词目，不复制词典释义或受版权保护的正文。

## 来源等级与取词边界

| 等级 | 来源 | 用法 |
| --- | --- | --- |
| A | 圣座、宗主教区、教区、宗派总部等官方资料 | 确定正式中文名称、信条、礼仪、圣事和教会制度术语 |
| B | 大学、研究机构和具编审制度的专业数据库 | 补人物、地名、古典语转写、历史教会和文献名称 |
| C | 已明确进入公版或采用开放许可证的文本 | 发现候选词并交叉核对，不当然复制整套数据 |
| D | 社群百科、商业词典、新闻和个人网站 | 只作线索，不凭单一页面直接入库 |

网页能够公开阅读不等于允许批量抓取或再分发。除非许可证明确兼容，本项目只
人工摘录不可版权化的短词目；释义、经文、长标题列表和数据库结构不复制。
现行组织名称和人物头衔还须回到对应教会官方网站复核。

## 天主教与东方礼天主教会

中文圣经人名、地名和书卷名以《思高圣经》传统为基准；教理、圣事、伦理、
教会论和祈祷术语以圣座繁体中文文献为第一依据。简体词形可以规范转换，但
不能把《和合本》的新教译名混入天主教专题词库。

- 圣座繁体中文《天主教教理》目录：核对教理、圣事、伦理、祈祷、圣统制和
  奉献生活等正式译语。
  https://www.vatican.va/chinese/ccc_zh.htm
- 圣座繁体中文梵蒂冈第二届大公会议文献：核对宪章、法令、宣言及教会论、
  礼仪、启示、合一和传教术语。
  https://www.vatican.va/chinese/concilio.htm
- 思高圣经学会及其网上圣经：核对天主教圣经书卷、人名、地名和固定译语。
  公开阅读不代表经文可自由再分发，本项目不复制经文正文。
  http://www.sbofmhk.org/
  http://www.sbofmhk.org/body/cpray/cpray.html
- 香港教区礼仪委员会：核对弥撒、圣事礼典、日课、礼仪年、圣仪和教区礼仪
  实务中的华语通行名称。
  http://catholic-dlc.org.hk/
- 天主教香港教区：核对教区机构、牧民指引、圣职与礼仪通告中的现行中文名称。
  https://catholic.org.hk/
- CNEWA *The Eastern Christian Churches*：由宗座机构发布的东方基督宗教教会
  概览，用于区分各东方礼天主教会、东正教、东方正统教会和东方亚述教会，
  特别适合核对礼仪传统、共融关系和教会层级；正文只作参考。
  https://cnewa.org/eastern-christian-churches/
- *Catholic Encyclopedia*（1913，New Advent 在线版）：可补拉丁术语、历史人物、
  修会和古代教区名称，但年代较早，现行制度与称谓必须再用圣座资料核对。
  https://www.newadvent.org/cathen/

`eosphoros.catholicism` 的既有大表还含早期人工整理词目；新增部分必须先进入
`catholicism_expansion_2026.txt`，通过编码、重码和跨库去重测试后再生成，不能
根据在线词典直接批量灌入。

## 新教与《和合本》

- CrossWire SWORD `ChiUns`：1919《和合本》简体数据，标为 Public Domain。
  https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=ChiUns
- Digital Bible Society《和合本》PDF：页面标注 Public Domain，用于复核书卷名、
  人名、地名和固定译语。
  https://bibles.dbs.org/CMNUNVS/pdf/CMNUNVS.pdf
- 信望爱圣经工具：提供《和合本》、原文字汇、语义词典和地理工具。站点声明
  CBOL 计划数据采用 GNU FDL，但部分内置词典另有出版社或编者来源；在逐项
  确认授权前仅作在线人工核对，不批量抓取释义。
  https://bible.fhl.net/gbdoc/index.html
- Book of Concord、LCMS、OPC、Anglican Communion、United Methodist Church
  的正式信条与教义页面，用于核对路德宗、改革宗、圣公宗和卫斯理宗术语。
  https://bookofconcord.org/
  https://www.lcms.org/about/beliefs/lutheran-confessions
  https://www.opc.org/GA/republication.html
  https://www.anglicancommunion.org/media/100850/ridley_cambridge_covenant_english.pdf
  https://www.umc.org/en/content/distinctive-wesleyan-emphases
- Global Anabaptist Mennonite Encyclopedia Online（GAMEO）：有编审制度的开放
  在线百科，用于再洗礼派、门诺会、阿米什和相关人物、会议、信条与机构名称。
  https://gameo.org/
- Hymnary.org：由 Calvin University 维护的圣诗、曲调、作者和诗集索引，适合
  核对圣诗名称与人物；歌词和乐谱授权各异，不复制正文或乐谱。
  https://hymnary.org/
- Christian Classics Ethereal Library（CCEL）：适合核对公版信条、宗教改革文献、
  旧译作者和作品名称；现代编辑内容仍须逐项查看版权说明。
  https://www.ccel.org/
- The Lutheran World Federation：核对世界信义宗联会、成员教会、全球共融与
  信义宗身份的现行名称。
  https://lutheranworld.org/who-we-are
- World Communion of Reformed Churches：覆盖改革宗、长老宗和公理宗成员教会，
  用于核对世界改革宗教会共融、区域议会与教会制度名称。
  https://wcrc.eu/about/
- Baptist World Alliance 的信仰声明与成员资料：核对浸信宗身份、信徒浸礼、
  地方教会自治和浸信会世界联盟等名称。
  https://baptistworld.org/beliefs/
- Friends World Committee for Consultation：贵格会的世界性官方组织，网站另有
  Quaker 术语表，适合核对朋友会、公谊会、静默崇拜和见证传统。
  https://fwcc.world/about-us/
- Mennonite World Conference：核对再洗礼派与门诺会的共同信念、世界大会、
  和平见证和跨国成员教会名称；GAMEO 用于补历史人物与机构。
  https://mwc-cmm.org/
- Unitas Fratrum：世界摩拉维亚弟兄会官方组织，用于核对合一弟兄会、教省、
  合一大会、赫恩胡特和每日箴言等本传统词目。
  https://www.unitasfratrum.org/
- University of Manchester Christian Brethren Collections：弟兄会史专业馆藏，
  用于核对普利茅斯弟兄会、开放弟兄会、闭关弟兄会和达秘等历史名称。
  https://www.library.manchester.ac.uk/rylands/special-collections/subject-areas/religion-and-theology/christian-brethren-collections/
- 香港及澳门救世军官方网站：核对救世军作为国际基督教教会所使用的大将、
  军官、军兵、部队及创办人等正式华语名称；网页正文不得转载。
  https://salvationarmy.org.hk/

循道卫理宗扩充部分另以中华基督教卫理公会、香港基督教循道卫理联合教会
和 United Methodist Communications 的公开资料核对中文会名、班会与联结
制度、议会体系、立约礼拜、亚德门经验、圣洁与恩典进程及历史人物；只摘取
词目，不复制文章正文：

- https://methodist.org.tw/john-wesley/
- https://methodist.org.tw/2024/01/18/question-1/
- https://methodist.org.tw/2024/01/11/%E9%99%84%E9%8C%84-%E6%88%90%E8%81%96/
- https://methodist.org.tw/dogma/
- https://www.methodist.org.hk/publications/monthlynews/?p=3
- https://www.umc.org/en/who-we-are/what-we-believe/our-wesleyan-heritage
- https://www.umc.org/en/content/organization-church-as-connection

《和合本》是 `eosphoros.protestantism` 的圣经中文基准；不用《思高本》或俄国
正教会汉译本替换其人名、地名和书卷名。书卷、人地名若已在本地基础词典中，
生成器只做去重，不在专题词库重复占码。

## 东正教

- Orthodox Church in America, *The Orthodox Faith* 与礼仪资料：神圣礼仪、
  圣奥迹、日课、礼仪年、圣像和自治制度。
  https://www.oca.org/orthodoxy/the-orthodox-faith
  https://www.oca.org/liturgics/outlines/definitions-and-sources
  https://www.oca.org/directories/world-churches
- Greek Orthodox Archdiocese of America 的两卷 *A Dictionary of Orthodox
  Terminology*：补礼仪书、圣职、教堂陈设、圣像、修道和希腊语转写词目。
  https://www.goarch.org/-/a-dictionary-of-orthodox-terminology-part-1
  https://www.goarch.org/-/a-dictionary-of-orthodox-terminology-part-2
- 普世宗主教区官方网站：复核现行宗主教区、圣统头衔、圣 synod 和正式机构名；
  非中文名称需与已有华语教会资料交叉核对后再定译名。
  https://ec-patr.org/

## 东方正统教会

- World Council of Churches 的 Oriental Orthodox church family 页面：正式共融
  名称、六大传统、前三次大公会议与合性论自我表述。
  https://www.oikoumene.org/church-families/orthodox-churches-oriental
- 科普特正教会、亚美尼亚使徒教会和叙利亚正教牧首区的官方网站，用于核对
  圣统、礼仪与本族语名称。
  https://copticorthodox.church/en/holysynod/
  https://www.armenianchurch.org/
  https://syriacpatriarchate.org/
- 埃塞俄比亚正统台瓦西多教会与印度马兰卡拉正教会官方网站：补齐现有来源
  对埃塞俄比亚、厄立特里亚和印度传统覆盖不足的问题，并复核台瓦西多、
  玛兰卡拉礼仪、教会节期和圣统名称。
  https://www.ethiopianorthodox.org/
  https://mosc.in/
- Claremont Colleges Digital Library 的 *Coptic Encyclopedia*：学术编纂的科普特
  历史、人物、地名、修道院和礼仪百科，只人工核对词目，不复制释义。
  https://ccdl.claremont.edu/digital/collection/cce
- Coptic Scriptorium：大学合作的科普特语数字人文项目，可核对古典语人地名、
  文献名和转写；进入中文词库前仍须有可靠中文译名。
  https://copticscriptorium.org/

不用“一性论”作为东方正统教会自称；历史研究中若确需收录争议旧称，应另作
明确标注，不能与“合性论”混同。

## 东方亚述教会与东方教会

- 东方亚述教会官方网站的介绍、礼仪资料和圣事对话文件，用于核对卡托利科斯
  牧首、阿代与马里礼仪、库尔巴纳、圣酵、拉泽圣事与东叙利亚传统。
  https://www.assyrianchurch.org/about-us/
  https://bethkokheh.assyrianchurch.org/wp-content/uploads/2016/10/Basic-Features-of-Liturgy.pdf
  https://news.assyrianchurch.org/wp-content/uploads/2017/11/Common-Statement-on-Sacramental-Life-FINAL-VERSION-18-NOV.pdf
- Syriaca.org：叙利亚文研究的学术参考门户，含人物、圣人、作者、地点和综合
  书目，采用 CC BY 4.0；适合核对规范名和异名，但中文译名仍需人工审定。
  https://syriaca.org/
- e-GEDSH（*Gorgias Encyclopedic Dictionary of the Syriac Heritage* 电子版）：
  由 Beth Mardutho 与多所大学学者编纂，适合核对东叙利亚、西叙利亚人物、
  牧首、文献和教会史术语；采用 CC BY-NC 4.0，因此这里只作非商业人工核对，
  不复制释义或整表。
  https://gedsh.bethmardutho.org/
- HMML Reading Room：可检索中东、印度等地叙利亚文手稿的规范题名、作者、
  抄写地和馆藏信息；影像与目录记录有各自使用条件，只作书目复核。
  https://www.vhmml.org/readingRoom/

景教史词目限于有文献根据的教会、人物、碑刻和写本名称；不把现代东方亚述
教会、古代东方教会、迦勒底天主教会或叙利亚正教会混为同一组织。

## 跨宗派与中国基督教史

下列资料不作为任何单一宗派的教义基准，但适合发现和交叉核对在华人物、机构、
学校、医院、出版物、会议和历史地名：

- Biographical Dictionary of Chinese Christianity（BDCC）：中英双语中国基督教
  人物传记库，适合核对中外人物姓名、间隔号写法和所属传统；正文受版权保护。
  https://www.bdcconline.net/
- China Historical Christian Database（CHCD）：记录 1550–1950 年中国基督教
  人物、机构与地点的学术数据库，适合发现异名和历史机构，不据其单一分类直接
  判断今天的宗派归属。
  https://chcdatabase.com/
- KU Leuven Chinese Christian Texts Database：中西文化接触相关中外文基督教
  原始、二手文献书目，适合核对书名、作者、出版机构和年代。
  https://www.arts.kuleuven.be/chinese-studies/english/cct
- World Council of Churches 的 church families 与 member churches 页面：适合
  核对普世教会组织采用的教会家族、正式成员名称和自我表述。
  https://www.oikoumene.org/church-families
  https://www.oikoumene.org/member-churches

这些跨宗派数据库提供的是检索线索。候选词最终必须回到所属教会的官方资料或
至少一个独立学术来源复核，并经过本项目的繁简规范、间隔号、键道六码、飞键、
跨库去重和重码预算检查。
