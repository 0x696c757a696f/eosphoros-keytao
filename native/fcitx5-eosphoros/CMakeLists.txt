cmake_minimum_required(VERSION 3.16)
project(fcitx5-eosphoros VERSION 0.1.0 LANGUAGES CXX)

include(GNUInstallDirs)
include(CTest)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

option(BUILD_FCITX_ADDON "Build and install the Fcitx5 addon" ON)
set(EOSPHOROS_DICTIONARY_MANIFEST
    "${CMAKE_CURRENT_SOURCE_DIR}/data/production-dictionaries.tsv"
    CACHE FILEPATH "Ordered repository dictionary manifest compiled into native data")
set(EOSPHOROS_SCHEMA
    "${CMAKE_CURRENT_SOURCE_DIR}/../../eosphoros.schema.yaml"
    CACHE FILEPATH "Rime schema whose topup/menu settings are compiled into native data")
file(GLOB EOSPHOROS_REPOSITORY_DICTIONARIES CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/../../dicts/eosphoros/*.dict.yaml")
file(GLOB EOSPHOROS_EMOJI_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/../../*cc/eosphoros/eosphoros_emoji*_*.lua")

set(NATIVE_DICTIONARY "${CMAKE_CURRENT_BINARY_DIR}/eosphoros-native.dict")
add_custom_command(
    OUTPUT "${NATIVE_DICTIONARY}"
    COMMAND "${Python3_EXECUTABLE}"
            "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_dictionary.py"
            --schema "${EOSPHOROS_SCHEMA}"
            --manifest "${EOSPHOROS_DICTIONARY_MANIFEST}"
            --root "${CMAKE_CURRENT_SOURCE_DIR}/../.."
            --output "${NATIVE_DICTIONARY}"
    DEPENDS "${EOSPHOROS_DICTIONARY_MANIFEST}"
            ${EOSPHOROS_REPOSITORY_DICTIONARIES}
            "${EOSPHOROS_SCHEMA}"
            "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_dictionary.py"
    VERBATIM)
add_custom_target(eosphoros-native-dictionary ALL DEPENDS "${NATIVE_DICTIONARY}")

set(NATIVE_AUXILIARY "${CMAKE_CURRENT_BINARY_DIR}/eosphoros-native.aux")
add_custom_command(
    OUTPUT "${NATIVE_AUXILIARY}"
    COMMAND "${Python3_EXECUTABLE}"
            "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_auxiliary.py"
            --pronunciation
            "${CMAKE_CURRENT_SOURCE_DIR}/../../dicts/eosphoros/eosphoros.cx.dict.yaml"
            --root "${CMAKE_CURRENT_SOURCE_DIR}/../.."
            --output "${NATIVE_AUXILIARY}"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_auxiliary.py"
            "${CMAKE_CURRENT_SOURCE_DIR}/../../dicts/eosphoros/eosphoros.cx.dict.yaml"
            ${EOSPHOROS_EMOJI_SOURCES}
    VERBATIM)
add_custom_target(eosphoros-native-auxiliary ALL DEPENDS "${NATIVE_AUXILIARY}")

add_library(eosphoros-native-core STATIC
    src/auxiliary.cpp
    src/context.cpp
    src/dictionary.cpp
    src/key_handler.cpp
    src/special.cpp
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
    install(FILES "${NATIVE_AUXILIARY}"
            DESTINATION "${FCITX_INSTALL_PKGDATADIR}/eosphoros-native")
    install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/../../assets/eosphoros-icon.png"
            RENAME fcitx-eosphoros-native.png
            DESTINATION "${CMAKE_INSTALL_DATADIR}/icons/hicolor/256x256/apps")
endif()

if(BUILD_TESTING)
    set(TEST_DICTIONARY "${CMAKE_CURRENT_BINARY_DIR}/eosphoros-native-test.dict")
    add_custom_command(
        OUTPUT "${TEST_DICTIONARY}"
        COMMAND "${Python3_EXECUTABLE}"
                "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_dictionary.py"
                --schema "${EOSPHOROS_SCHEMA}"
                --input "${CMAKE_CURRENT_SOURCE_DIR}/tests/fixtures/minimal.dict.yaml"
                --output "${TEST_DICTIONARY}"
        DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/tests/fixtures/minimal.dict.yaml"
                "${EOSPHOROS_SCHEMA}"
                "${CMAKE_CURRENT_SOURCE_DIR}/tools/build_dictionary.py"
        VERBATIM)
    add_custom_target(eosphoros-native-test-dictionary DEPENDS "${TEST_DICTIONARY}")
    add_executable(eosphoros-native-dictionary-test tests/test_dictionary.cpp)
    target_link_libraries(eosphoros-native-dictionary-test PRIVATE eosphoros-native-core)
    add_dependencies(eosphoros-native-dictionary-test eosphoros-native-test-dictionary)
    add_test(NAME eosphoros-native-dictionary
        COMMAND eosphoros-native-dictionary-test "${TEST_DICTIONARY}")

    add_executable(eosphoros-native-topup-test tests/test_topup.cpp)
    target_link_libraries(eosphoros-native-topup-test PRIVATE eosphoros-native-core)
    add_test(NAME eosphoros-native-topup COMMAND eosphoros-native-topup-test)

    add_executable(eosphoros-native-special-test tests/test_special.cpp)
    target_link_libraries(eosphoros-native-special-test PRIVATE eosphoros-native-core)
    add_test(NAME eosphoros-native-special COMMAND eosphoros-native-special-test)

    add_executable(eosphoros-native-context-test tests/test_context.cpp)
    target_link_libraries(eosphoros-native-context-test PRIVATE eosphoros-native-core)
    add_dependencies(eosphoros-native-context-test eosphoros-native-test-dictionary)
    add_test(NAME eosphoros-native-context
        COMMAND eosphoros-native-context-test "${TEST_DICTIONARY}"
                "${CMAKE_CURRENT_SOURCE_DIR}/tests/golden/normal.tsv")

    add_executable(eosphoros-native-production-dictionary-test
        tests/test_production_dictionary.cpp)
    target_link_libraries(eosphoros-native-production-dictionary-test
        PRIVATE eosphoros-native-core)
    add_dependencies(eosphoros-native-production-dictionary-test
        eosphoros-native-dictionary)
    add_test(NAME eosphoros-native-production-dictionary
        COMMAND eosphoros-native-production-dictionary-test "${NATIVE_DICTIONARY}")

    add_executable(eosphoros-native-auxiliary-test tests/test_auxiliary.cpp)
    target_link_libraries(eosphoros-native-auxiliary-test PRIVATE eosphoros-native-core)
    add_dependencies(eosphoros-native-auxiliary-test eosphoros-native-auxiliary
                     eosphoros-native-dictionary)
    add_test(NAME eosphoros-native-auxiliary
        COMMAND eosphoros-native-auxiliary-test "${NATIVE_AUXILIARY}"
                "${NATIVE_DICTIONARY}")
endif()
