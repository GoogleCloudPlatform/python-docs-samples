cc_library(
    name = "hsm_functions",
    srcs = ["hsm_functions.cc"],
    hdrs = ["hsm_functions.h"],
    deps = [
        "//cloud/security/hawksbill/cavium:cavium_api_interface_header",
        "//cloud/security/hawksbill/cavium:cavium_api_shim",
        "//testing/base/public:gunit_headers",
        "//third_party/absl/log:check",
        "//third_party/absl/status",
        "//third_party/absl/status:statusor",
        "//third_party/absl/strings",
        "//third_party/cavium_hsm/v3_4__14:cavium_hsm",
        "//third_party/cavium_hsm/v3_4__14/utils:openssl_util",
        "//third_party/openssl:crypto",
        "//util/task:status",
    ],
)

cc_test(
    name = "hsm_functions_test",
    srcs = ["hsm_functions_test.cc"],
    deps = [
        ":hsm_functions",
        "//base:raw_logging",
        "//cloud/security/hawksbill/cavium:cavium_api_shim",
        "//cloud/security/hawksbill/cavium:lib_cavium",
        "//testing/base/public:gunit_main",
        "//third_party/absl/log",
        "//third_party/absl/status:statusor",
        "//third_party/absl/strings",
        "//third_party/openssl:crypto",
        "//util/task:status",
    ],
)

cc_binary(
    name = "hsm_functions_perf_test",
    srcs = ["hsm_functions_perf_test.cc"],
    deps = [
        ":hsm_functions",
        "//testing/base/public:gunit",
        "//third_party/openssl:crypto",
    ],
)

cc_test(
    name = "cavium_layers_test",
    srcs = ["cavium_layers_test.cc"],
    deps = [
        ":hsm_functions",
        "//base:raw_logging",
        "//cloud/security/hawksbill/cavium:cavium_api_error",
        "//cloud/security/hawksbill/cavium:cavium_api_error_enum",
        "//cloud/security/hawksbill/cavium:cavium_api_shim",
        "//cloud/security/hawksbill/cavium:lib_cavium",
        "//testing/base/public:gunit_main",
        "//third_party/absl/strings",
    ],
)
