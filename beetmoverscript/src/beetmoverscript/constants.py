MIME_MAP = {
    "": "text/plain",
    ".aab": "application/octet-stream",
    ".aar": "application/java-archive",
    ".apk": "application/vnd.android.package-archive",
    ".asc": "text/plain",
    ".beet": "text/plain",
    ".bundle": "application/octet-stream",
    ".bz2": "application/octet-stream",
    ".checksums": "text/plain",
    ".dmg": "application/x-iso9660-image",
    ".log": "text/plain",
    ".jar": "application/java-archive",
    ".json": "application/json",
    ".mar": "application/octet-stream",
    ".md5": "text/plain",
    ".module": "application/json",
    ".msi": "application/x-msi",
    # Per https://docs.microsoft.com/en-us/windows/msix/app-installer/web-install-iis
    ".msix": "application/msix",
    ".pkg": "application/x-newton-compatible-pkg",
    ".pom": "application/xml",
    ".rcc": "application/octet-stream",
    ".sha1": "text/plain",
    ".sha256": "text/plain",
    ".sha512": "text/plain",
    ".sig": "application/octet-stream",
    ".snap": "application/octet-stream",
    ".xpi": "application/x-xpinstall",
    ".xz": "application/x-xz",
}

STAGE_PLATFORM_MAP = {
    "linux": "linux-i686",
    "linux-devedition": "linux-i686",
    "linux64": "linux-x86_64",
    "linux64-asan-reporter": "linux-x86_64-asan-reporter",
    "linux64-devedition": "linux-x86_64",
    "macosx64": "mac",
    "macosx64-asan-reporter": "mac-asan-reporter",
    "macosx64-devedition": "mac",
    "win32-devedition": "win32",
    "win64-devedition": "win64",
    "win64-aarch64-devedition": "win64-aarch64",
}

NORMALIZED_BALROG_PLATFORMS = {
    "linux-devedition": "linux",
    "linux64-devedition": "linux64",
    "macosx64-devedition": "macosx64",
    "win32-devedition": "win32",
    "win64-devedition": "win64",
    "win64-aarch64-devedition": "win64-aarch64",
}

NORMALIZED_FILENAME_PLATFORMS = NORMALIZED_BALROG_PLATFORMS.copy()
NORMALIZED_FILENAME_PLATFORMS.update(
    {
        "android": "android-arm",
        "android-api-15": "android-arm",
        "android-api-15-old-id": "android-arm",
        "android-api-16": "android-arm",
        "android-api-16-old-id": "android-arm",
        "android-x86": "android-i386",
        "android-x86-old-id": "android-i386",
        "android-aarch64": "android-aarch64",
    }
)

HASH_BLOCK_SIZE = 1024 * 1024

RELEASE_BRANCHES = ("mozilla-central", "mozilla-beta", "mozilla-release", "mozilla-esr102", "comm-central", "comm-beta", "comm-esr102")

# actions that imply actual releases, hence the need of `build_number` and
# `version`
PROMOTION_ACTIONS = ("push-to-candidates",)

RELEASE_ACTIONS = ("push-to-releases",)

DIRECT_RELEASE_ACTIONS = ("direct-push-to-bucket",)

PARTNER_REPACK_ACTIONS = ("push-to-partner",)

MAVEN_ACTIONS = ("push-to-maven",)

ARTIFACT_REGISTRY_ACTIONS = ("import-from-gcs-to-artifact-registry",)

# XXX this is a fairly clunky way of specifying which files to copy from
# candidates to releases -- let's find a nicer way of doing this.
# XXX if we keep this, let's make it configurable? overridable in config?
# Faster to update a config file in puppet than to ship a new beetmover release
# and update in puppet
RELEASE_EXCLUDE = (
    r"^.*tests.*$",
    r"^.*crashreporter.*$",
    r"^(?!.*jsshell-).*\.zip(\.asc)?$",
    r"^.*\.log$",
    r"^.*\.txt$",
    r"^.*/partner-repacks.*$",
    r"^.*.checksums(\.asc)?$",
    r"^.*/logs/.*$",
    r"^.*json$",
    r"^.*/host.*$",
    r"^.*/mar-tools/.*$",
    r"^.*contrib.*",
    r"^.*/beetmover-checksums/.*$",
)

CACHE_CONTROL_MAXAGE = 3600 * 4

PRODUCT_TO_PATH = {
    "devedition": "pub/devedition/",
    "fenix": "pub/fenix/",
    "firefox": "pub/firefox/",
    "focus": "pub/focus/",
    "thunderbird": "pub/thunderbird/",
    "vpn": "pub/vpn/",
}

MAVEN_PRODUCT_TO_PATH = {
    "appservices": "maven2/org/mozilla/appservices/",
    "components": "maven2/org/mozilla/components/",
    "nightly_components": "maven2/org/mozilla/components/",
    "geckoview": "maven2/org/mozilla/geckoview/",
    "telemetry": "maven2/org/mozilla/telemetry/",
}

PARTNER_REPACK_PREFIX_TMPL = "pub/firefox/candidates/{version}-candidates/build{build_number}/"
PARTNER_REPACK_REGEXES = (
    r"^(beetmover-checksums\/)?(mac|win32|win64(|-aarch64))-EME-free\/[^\/.]+$",
    r"^partner-repacks\/(?P<partner>[^\/%]+)\/(?P<subpartner>[^\/%]+)\/v\d+\/(mac|win32|win64(|-aarch64)|linux-i686|linux-x86_64)\/(?P<locale>[^\/%]+)$",
)

CHECKSUMS_CUSTOM_FILE_NAMING = {"beetmover-source": "-source", "release-beetmover-signed-langpacks": "-langpack"}

BUILDHUB_ARTIFACT = "buildhub.json"

# the installer artifact for each platform
INSTALLER_ARTIFACTS = ("target.tar.bz2", "target.tar.xz", "target.installer.exe", "target.dmg", "target.apk")
