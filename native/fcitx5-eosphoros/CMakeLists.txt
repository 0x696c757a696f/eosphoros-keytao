cmake_minimum_required(VERSION 3.16)
project(fcitx5-eosphoros VERSION 0.1.0 LANGUAGES CXX)

include(GNUInstallDirs)
include(CTest)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

option(BUILD_FCITX_ADDON "Build and install the Fcitx5 addon" ON)
set(EOSPHOROS_DICTIONARY_INPUTS
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/fixtures/minimal.dict.yaml"
    CACHE STRING "Semicolon-separated Rime dictionaries compiled into native data")

set(NATIVE_DICTIONARY "${CMAKE_CURRENT_BINARY_DIR}/eosphoros-native.dict")
set(DICTIONARY_ARGS)
foreach(DICTIONARY_INPUT IN LISTS EOSPHOROS_DICTIONARY_INPUTS)
    list(APPEND DICTIONARY_ARGS --input "${DICTIONARY_INPUT}")
endforeach()
add_custom_command(
    OUTPUT "${NATIVE_DICTIONARY}"
    COMMAND "${Python3_EXECUTABLE}"
            "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_dictionary.py"
            ${DICTIONARY_ARGS} --output "${NATIVE_DICTIONARY}"
    DEPENDS ${EOSPHOROS_DICTIONARY_INPUTS}
            "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_dictionary.py"
    VERBATIM)
add_custom_target(eosphoros-native-dictionary ALL DEPENDS "${NATIVE_DICTIONARY}")

add_library(eosphoros-native-core STATIC
    src/context.cpp
    src/dictionary.cpp
    src/key_handler.cpp
    src/topup.cpp)
target_include_directories(eosphoros-native-core PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/src")
target_compile_features(eosphoros-native-core PUBLIC cxx_std_17)
set_target_properties(eosphoros-native-core PROPERTIES POSITION_INDEPENDENT_CODE ON)

if(BUILD_FCITX_ADDON)
    set(REQUIRED_FCITX_VERSION 5.1.7)
    find_package(ECM REQUIRED 1.0.0)
    set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${CMAKE_MODULE_PATH})
    find_package(Fcitx5Core ${REQUIRED_FCITX_VERSION} REQUIRED)
    include("${Fcitx5Utils_DIR}/Fcitx5CompilerSettings.cmake")

    add_library(eosphoros-native MODULE
        src/addon.cpp
        src/candidate.cpp
        src/engine.cpp)
    target_link_libraries(eosphoros-native
        eosphoros-native-core
        Fcitx5::Core)
    target_compile_features(eosphoros-native PRIVATE cxx_std_17)
    set_target_properties(eosphoros-native PROPERTIES
        CXX_VISIBILITY_PRESET hidden
        VISIBILITY_INLINES_HIDDEN ON)

    configure_file(data/eosphoros-native-addon.conf.in
                   eosphoros-native-addon.conf @ONLY)
    configure_file(data/eosphoros-native.conf.in eosphoros-native.conf @ONLY)

    install(TARGETS eosphoros-native DESTINATION "${FCITX_INSTALL_ADDONDIR}")
    install(FILES "${CMAKE_CURRENT_BINARY_DIR}/eosphoros-native-addon.conf"
            RENAME eosphoros-native.conf
            DESTINATION "${FCITX_INSTALL_PKGDATADIR}/addon")
    install(FILES "${CMAKE_CURRENT_BINARY_DIR}/eosphoros-native.conf"
            DESTINATION "${FCITX_INSTALL_PKGDATADIR}/inputmethod")
    install(FILES "${NATIVE_DICTIONARY}"
            DESTINATION "${FCITX_INSTALL_PKGDATADIR}/eosphoros-native")
    install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/../../assets/eosphoros-icon.png"
            RENAME fcitx-eosphoros-native.png
            DESTINATION "${CMAKE_INSTALL_DATADIR}/icons/hicolor/256x256/apps")
endif()

if(BUILD_TESTING)
    add_executable(eosphoros-native-core-test tests/test_core.cpp)
    target_link_libraries(eosphoros-native-core-test PRIVATE eosphoros-native-core)
    add_dependencies(eosphoros-native-core-test eosphoros-native-dictionary)
    add_test(NAME eosphoros-native-core
        COMMAND eosphoros-native-core-test "${NATIVE_DICTIONARY}"
                "${CMAKE_CURRENT_SOURCE_DIR}/tests/golden/normal.tsv")
endif()
