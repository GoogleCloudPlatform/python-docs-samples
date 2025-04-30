#include "experimental/users/brandonluong/asr/hsm_functions.h"

#include <cstdint>
#include <vector>

#include "third_party/absl/log/check.h"
#include "third_party/absl/status/status.h"
#include "third_party/absl/status/statusor.h"
#include "third_party/absl/strings/escaping.h"
#include "third_party/absl/strings/substitute.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_args.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_defines.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_errors.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_mgmt.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_structs.h"
#include "third_party/cavium_hsm/v3_4__14/cavium_wrappers.h"
#include "third_party/cavium_hsm/v3_4__14/utils/openssl_util.h"
#include "third_party/openssl/bn.h"
#include "third_party/openssl/ec.h"
#include "third_party/openssl/ec_key.h"
#include "third_party/openssl/rand.h"
#include "third_party/openssl/rsa.h"

#define CHECK_SUCCESS(expr)                      \
  {                                              \
    int32_t ret = expr;                          \
    CHECK_EQ(ret, 0) << Cfm2ResultAsString(ret); \
  }

namespace third_party_cavium_hsm {

std::vector<uint8_t> RandomLabel() {
  uint8_t rand[16];
  RAND_bytes(rand, sizeof(rand));
  std::string hex = absl::BytesToHexString(
      absl::string_view(reinterpret_cast<char*>(rand), sizeof(rand)));
  CHECK_EQ(hex.size(), 32);
  return std::vector<uint8_t>(hex.begin(), hex.end());
}

uint32_t Test_Init() {
  uint32_t application_handle;
  Cfm2Initialize2(167936, DIRECT, &application_handle);

  return application_handle;
}

uint32_t Initialize() {
  uint32_t application_handle;
  CHECK_SUCCESS(Cfm2Initialize2(0, DIRECT, &application_handle));

  uint32_t session_handle;
  CHECK_SUCCESS(Cfm2OpenSession2(application_handle, &session_handle));

  constexpr absl::string_view kUsername = "crypto_user";
  constexpr absl::string_view kPassword = "user123";

  std::vector<uint8_t> encrypted_password(PSWD_ENC_KEY_MODULUS, 0);
  uint32_t password_size = encrypted_password.size();
  CHECK_SUCCESS(utils::encrypt_pswd(
      session_handle,
      reinterpret_cast<uint8_t*>(const_cast<char*>(kPassword.data())),
      kPassword.size(), encrypted_password.data(), &password_size));
  encrypted_password.resize(password_size);

  CHECK_SUCCESS(Cfm2LoginHSM2(
      session_handle, CN_CRYPTO_USER,
      reinterpret_cast<uint8_t*>(const_cast<char*>(kUsername.data())),
      kUsername.size(), encrypted_password.data(), encrypted_password.size(),
      /*signature=*/nullptr));

  return application_handle;
}

uint32_t OpenSession(uint32_t application_handle) {
  uint32_t session_handle;
  CHECK_SUCCESS(Cfm2OpenSession2(application_handle, &session_handle));
  return session_handle;
}

void CloseSession(uint32_t session_handle) {
  CHECK_SUCCESS(Cfm2CloseSession(session_handle));
}

uint64_t GenerateParkingKey(uint32_t session_handle) {
  std::vector<uint8_t> label = RandomLabel();

  genKeyArgs args = {0};
  args.ulSessionHandle = session_handle;
  args.key.info.ucKeyLocation = STORAGE_FLASH;
  args.key.info.ulKeyType = KEY_TYPE_AES;
  args.key.info.ulKeyLen = 32;
  args.key.info.bParking = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  CHECK_SUCCESS(CfmGenerateKey(&args));
  return args.key.ulKeyHandle;
}

uint64_t GenerateAesWrappingKey(uint32_t session_handle) {
  std::vector<uint8_t> label = RandomLabel();

  genKeyArgs args = {0};
  args.ulSessionHandle = session_handle;
  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyType = KEY_TYPE_AES;
  args.key.info.ulKeyLen = 32;
  args.key.info.ulKeyClass = OBJ_CLASS_SECRET_KEY;
  args.key.info.ulMValue = 1;
  args.key.info.bExtractable = 0;
  args.key.info.bParkable = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();

  default_attributes(&args.key.info);
  CHECK_SUCCESS(CfmGenerateKey(&args));
  return args.key.ulKeyHandle;
}

uint64_t GenerateExtractableSymmetricKey(uint32_t session_handle,
                                         SymmetricKeyType key_type) {
  std::vector<uint8_t> label = RandomLabel();

  genKeyArgs args = {0};
  args.ulSessionHandle = session_handle;
  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyClass = OBJ_CLASS_SECRET_KEY;
  args.key.info.ulMValue = 1;
  args.key.info.bExtractable = 1;
  args.key.info.bParkable = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  switch (key_type) {
    case SymmetricKeyType::kAes256:
      args.key.info.ulKeyType = KEY_TYPE_AES;
      args.key.info.ulKeyLen = 32;
      break;
    case SymmetricKeyType::kHkdfSha256:
      args.key.info.ulKeyType = KEY_TYPE_GENERIC_SECRET;
      args.key.info.ulKeyLen = 32;
      args.key.info.ucDerive = 1;
      break;
  }

  default_attributes(&args.key.info);
  CHECK_SUCCESS(CfmGenerateKey(&args));
  return args.key.ulKeyHandle;
}

KeyPair GenerateEcdhKeypair(uint32_t session_handle, int curve) {
  std::vector<uint8_t> label = RandomLabel();

  genKeyArgs args = {0};
  args.ulSessionHandle = session_handle;

  args.pubkey.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.pubkey.info.bParkable = 1;
  args.pubkey.info.ulKeyClass = OBJ_CLASS_PUBLIC_KEY;
  args.pubkey.info.ulCurveID = curve;
  args.pubkey.info.ulMValue = 1;
  args.pubkey.info.pLabel = label.data();
  args.pubkey.info.ulLabelLen = label.size();
  args.pubkey.info.ulKeyType = KEY_TYPE_EC;
  args.pubkey.info.ucDerive = 1;
  default_attributes(&args.pubkey.info);

  args.privkey.info.ulKeyClass = OBJ_CLASS_PRIVATE_KEY;
  args.privkey.info.ulCurveID = args.pubkey.info.ulCurveID;
  args.privkey.info.ulKeyType = args.pubkey.info.ulKeyType;
  args.privkey.info.ucDerive = 1;

  copy_public_attr_to_priv_attr(&args);

  CHECK_SUCCESS(CfmGenerateKeyPair(&args));
  return {.pub = args.pubkey.ulKeyHandle, .prv = args.privkey.ulKeyHandle};
}

std::vector<uint8_t> ParkKey(uint32_t session_handle,
                             uint64_t parking_key_handle,
                             uint64_t target_key_handle) {
  uint8_t buffer[6000];  // as hardcoded in Cfm2Util

  parkOpArgs args = {0};
  args.pParkedObject = buffer;
  args.ulParkedObjectLen = sizeof(buffer);
  args.ulSessionHandle = session_handle;
  args.ulParkingKeyHandle = parking_key_handle;
  args.ulObjectHandle = target_key_handle;
  CHECK_SUCCESS(CfmParkObject(&args));

  uint8_t* parked_key_start = GET_KEY1_ATTR(args.pParkedObject);
  return std::vector<uint8_t>(parked_key_start,
                              parked_key_start + args.ulParkedObjectLen);
}

uint64_t UnparkKey(uint32_t session_handle, uint64_t parking_key_handle,
                   std::vector<uint8_t>& parked_key) {
  unparkOpArgs args = {0};
  args.pParkedObject = parked_key.data();
  args.ulParkedObjectLen = parked_key.size();
  args.ulSessionHandle = session_handle;
  args.ulParkingKeyHandle = parking_key_handle;
  args.ephemeralStorage = 1;
  CHECK_SUCCESS(CfmUnparkObject(&args));
  return args.ulObjectHandle;
}

void InitializeWrapArgs(third_party_cavium_interface::WrapArguments pArgs) {
  // size fails at 8925, Cfm2Util hardcoded max is 8192
  uint8_t buffer[8924];  // as hardcoded in Cfm2Util
  uint32_t app_handle = Initialize();
  uint32_t session_handle = OpenSession(app_handle);
  uint32_t wrapping_key_handle = GenerateAesWrappingKey(session_handle);
  absl::StatusOr<uint32_t> target_key_handle = GenerateExtractableSymmetricKey(
      session_handle, SymmetricKeyType::kAes256);
  uint32_t aes_key_wrap_pad = 0x00001091;

  // input args
  pArgs.common.session_handle = session_handle;
  pArgs.common.wrapping_key_handle = wrapping_key_handle;
  pArgs.common.mech = aes_key_wrap_pad;
  pArgs.common.key.ul_key_handle = target_key_handle.value();
  pArgs.common.key_input_output =
      third_party_cavium_interface::CaviumInputType::CAVIUM_ENCRYPTED;

  // output args
  pArgs.wrapped_key = buffer;
  pArgs.wrapped_key_len = sizeof(buffer);
}

std::vector<uint8_t> WrapKeyAesKwp(uint32_t session_handle,
                                   uint64_t wrapping_key_handle,
                                   uint64_t target_key_handle) {
  uint8_t buffer[MAX_DATA_LENGTH];  // as hardcoded in Cfm2Util

  wrapArgs args = {0};
  args.aes_key_len = AES_256_KEY_SIZE;
  args.KeyOutput = ENCRYPTED;
  args.ulMech = CRYPTO_MECH_AES_KEY_WRAP_PAD;
  args.ulWrappingKeyHandle = wrapping_key_handle;
  args.key.ulKeyHandle = target_key_handle;
  args.pKey = buffer;
  args.ulKeyLen = sizeof(buffer);
  args.ulSessionHandle = session_handle;
  CHECK_SUCCESS(CfmWrap(&args));

  return std::vector<uint8_t>(buffer, buffer + args.ulKeyLen);
}

void WrapKeySmallBuffer(uint32_t session_handle, uint64_t wrapping_key_handle,
                        uint64_t target_key_handle, int wrapped_key_len) {
  uint8_t buffer[7000];  // as hardcoded in Cfm2Util

  wrapArgs args = {0};
  args.aes_key_len = AES_256_KEY_SIZE;
  args.KeyOutput = ENCRYPTED;
  args.ulMech = CRYPTO_MECH_AES_KEY_WRAP_PAD;
  args.ulWrappingKeyHandle = wrapping_key_handle;
  args.key.ulKeyHandle = target_key_handle;
  args.pKey = buffer;
  args.ulKeyLen = 7050;
  args.ulSessionHandle = session_handle;
  CHECK_SUCCESS(CfmWrap(&args));
  // CfmWrap(&args);

  // return std::vector<uint8_t>(buffer, buffer + args.ulKeyLen);
}

std::vector<uint8_t> WrapKeyRsaOaep(uint32_t session_handle,
                                    uint64_t wrapping_key_handle,
                                    uint64_t target_key_handle) {
  uint8_t buffer[MAX_DATA_LENGTH];  // as hardcoded in Cfm2Util

  wrapArgs args = {0};
  args.KeyOutput = ENCRYPTED;
  args.ulMech = CRYPTO_MECH_RSA_OAEP_KEY_WRAP;
  args.hash_type = HashType::SHA256_TYPE;
  args.ulWrappingKeyHandle = wrapping_key_handle;
  args.key.ulKeyHandle = target_key_handle;
  args.pKey = buffer;
  args.ulKeyLen = sizeof(buffer);
  args.ulSessionHandle = session_handle;
  CHECK_SUCCESS(CfmWrap(&args));

  return std::vector<uint8_t>(buffer, buffer + args.ulKeyLen);
}

absl::StatusOr<uint64_t> UnwrapKeyAesKwp(uint32_t session_handle,
                                         uint64_t wrapping_key_handle,
                                         std::vector<uint8_t>& wrapped_key,
                                         SymmetricKeyType key_type) {
  std::vector<uint8_t> label = RandomLabel();

  unwrapArgs args = {0};

  args.aes_key_len = AES_256_KEY_SIZE;
  args.KeyOutput = ENCRYPTED;
  args.ulMech = CRYPTO_MECH_AES_KEY_WRAP_PAD;
  args.ulWrappingKeyHandle = wrapping_key_handle;
  args.pKey = wrapped_key.data();
  args.ulKeyLen = wrapped_key.size();
  args.ulSessionHandle = session_handle;

  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyClass = OBJ_CLASS_SECRET_KEY;
  args.key.info.ulMValue = 1;
  args.key.info.bExtractable = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  switch (key_type) {
    case SymmetricKeyType::kAes256:
      args.key.info.ulKeyType = KEY_TYPE_AES;
      args.key.info.ulKeyLen = 32;
      break;
    case SymmetricKeyType::kHkdfSha256:
      args.key.info.ulKeyType = KEY_TYPE_GENERIC_SECRET;
      args.key.info.ulKeyLen = 32;
      args.key.info.ucDerive = 1;
      break;
  }
  default_attributes(&args.key.info);
  int32_t ret = CfmUnwrap(&args);
  if (ret == 0) {
    return args.key.ulKeyHandle;
  } else {
    return absl::InternalError(absl::Substitute("Cavium Error"));
  }
}

absl::StatusOr<uint64_t> UnwrapKeyAesKnp(uint32_t session_handle,
                                         uint64_t wrapping_key_handle,
                                         std::vector<uint8_t>& wrapped_key,
                                         SymmetricKeyType key_type) {
  std::vector<uint8_t> label = RandomLabel();

  unwrapArgs args = {0};

  args.aes_key_len = AES_256_KEY_SIZE;
  args.KeyOutput = ENCRYPTED;
  args.ulMech = CRYPTO_MECH_AES_KEY_WRAP;
  args.ulWrappingKeyHandle = wrapping_key_handle;
  args.pKey = wrapped_key.data();
  args.ulKeyLen = wrapped_key.size();
  args.ulSessionHandle = session_handle;

  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyClass = OBJ_CLASS_SECRET_KEY;
  args.key.info.ulMValue = 1;
  args.key.info.bExtractable = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  switch (key_type) {
    case SymmetricKeyType::kAes256:
      args.key.info.ulKeyType = KEY_TYPE_AES;
      args.key.info.ulKeyLen = 32;
      break;
    case SymmetricKeyType::kHkdfSha256:
      args.key.info.ulKeyType = KEY_TYPE_GENERIC_SECRET;
      args.key.info.ulKeyLen = 32;
      args.key.info.ucDerive = 1;
      break;
  }
  default_attributes(&args.key.info);
  int32_t ret = CfmUnwrap(&args);
  if (ret == 0) {
    return args.key.ulKeyHandle;
  } else {
    return absl::InternalError(absl::Substitute("Cavium Error"));
  }
}

uint64_t DeriveAes256KeyHkdfSha256(uint32_t session_handle, uint64_t key_handle,
                                   std::vector<uint8_t> info) {
  std::vector<uint8_t> label = RandomLabel();

  deriveKeyArgs args = {0};
  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyClass = OBJ_CLASS_SECRET_KEY;
  args.key.info.ulMValue = 1;
  args.key.info.bExtractable = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  args.key.info.ulKeyType = KEY_TYPE_AES;
  args.key.info.ulKeyLen = 32;
  default_attributes(&args.key.info);

  args.ulSessionHandle = session_handle;
  args.hBaseKey = key_handle;
  constexpr uint64_t kCkdSha256Kdf = 0x06UL;
  args.ulDeriveMech =
      CRYPTO_MECH_LIQ_SEC(DERIVE_MECH_HKDF) + (kCkdSha256Kdf << 16);
  args.prfCtx = info.data();
  args.ulPrfCtxLen = info.size();
  args.ulDKMLengthMethod = SP800_108_DKM_LENGTH_SUM_OF_KEYS;

  CHECK_SUCCESS(CfmDeriveKey(&args));
  return args.key.ulKeyHandle;
}

uint64_t DeriveAes256KeyEcdhHkdfSha256(uint32_t session_handle,
                                       uint64_t local_private_key_handle,
                                       EC_KEY* remote_public_key) {
  std::vector<uint8_t> label = RandomLabel();

  deriveKeyArgs args = {0};
  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyClass = OBJ_CLASS_SECRET_KEY;
  args.key.info.ulMValue = 1;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  args.key.info.ulKeyType = KEY_TYPE_AES;
  args.key.info.ulKeyLen = 32;
  default_attributes(&args.key.info);

  args.ulSessionHandle = session_handle;
  args.hBaseKey = local_private_key_handle;
  constexpr uint64_t kCkdSha256Kdf = 0x06UL;
  args.ulDeriveMech =
      CRYPTO_MECH_LIQ_SEC(DERIVE_MECH_ECDH_HKDF) + (kCkdSha256Kdf << 16);
  args.ulDKMLengthMethod = SP800_108_DKM_LENGTH_SUM_OF_KEYS;

  std::vector<uint8_t> serialized_remote_public_key;

  serialized_remote_public_key.resize(
      EC_POINT_point2oct(EC_KEY_get0_group(remote_public_key),
                         EC_KEY_get0_public_key(remote_public_key),
                         POINT_CONVERSION_UNCOMPRESSED, nullptr, 0, nullptr));
  CHECK_EQ(EC_POINT_point2oct(EC_KEY_get0_group(remote_public_key),
                              EC_KEY_get0_public_key(remote_public_key),
                              POINT_CONVERSION_UNCOMPRESSED,
                              serialized_remote_public_key.data(),
                              serialized_remote_public_key.size(), nullptr),
           serialized_remote_public_key.size());
  args.pPubKey = serialized_remote_public_key.data();
  args.ulPubKeyLen = serialized_remote_public_key.size();

  CHECK_SUCCESS(CfmDeriveKey(&args));
  return args.key.ulKeyHandle;
}

bssl::UniquePtr<EC_KEY> ExportEcPublicKey(uint32_t session_handle,
                                          uint64_t key_handle, int curve_id) {
  bssl::UniquePtr<EC_GROUP> group(EC_GROUP_new_by_curve_name(curve_id));
  CHECK_NE(group, nullptr);

  uint32_t buf_length = 1024;
  std::vector<uint8_t> buf;
  buf.resize(buf_length);

  CHECK_SUCCESS(
      Cfm2ExportPublicKey(session_handle, key_handle, buf.data(), &buf_length));

  bssl::UniquePtr<EC_KEY> key(EC_KEY_new());
  CHECK_NE(key, nullptr);
  CHECK_EQ(EC_KEY_set_group(key.get(), group.get()), 1);

  bssl::UniquePtr<EC_POINT> point(EC_POINT_new(group.get()));
  CHECK_NE(point, nullptr);
  CHECK_EQ(EC_POINT_oct2point(group.get(), point.get(), buf.data(), buf_length,
                              nullptr),
           1);

  CHECK_EQ(EC_KEY_set_public_key(key.get(), point.get()), 1);

  return key;
}

void DeleteKey(uint32_t session_handle, uint64_t key_handle) {
  CHECK_SUCCESS(Cfm2DeleteKey(session_handle, key_handle));
}

uint64_t ImportRsaPublicKey(uint32_t session_handle, const RSA* rsa_pub) {
  CHECK_NE(rsa_pub, nullptr);

  std::vector<uint8_t> label = RandomLabel();

  genKeyArgs args = {0};

  args.ulSessionHandle = session_handle;
  args.key.info.ucKeyLocation = STORAGE_EPHEMERAL;
  args.key.info.ulKeyClass = OBJ_CLASS_PUBLIC_KEY;
  args.key.info.pLabel = label.data();
  args.key.info.ulLabelLen = label.size();
  args.key.info.ulKeyType = KEY_TYPE_RSA;

  const BIGNUM *n, *e, *d;
  RSA_get0_key(rsa_pub, &n, &e, &d);
  CHECK_NE(n, nullptr);
  CHECK_NE(e, nullptr);

  std::vector<uint8_t> modulus;
  modulus.resize(BN_num_bytes(n));
  BN_bn2bin(n, modulus.data());
  args.key.info.pModulus = modulus.data();
  args.key.info.ulModLenInBits = modulus.size() * 8;

  uint64_t pub_exp;
  CHECK_EQ(BN_get_u64(e, &pub_exp), 1);
  args.key.info.ulPubExp = pub_exp;

  default_attributes(&args.key.info);

  CHECK_SUCCESS(CfmCreateObject(&args));
  return args.key.ulKeyHandle;
}

}  // namespace third_party_cavium_hsm
