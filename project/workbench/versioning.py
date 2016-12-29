from rest_framework.versioning import URLPathVersioning


class AllVersioning(URLPathVersioning):
    default_version = "v1"
    allowed_versions = [None, "v1", "v2"]
    version_param = "version"
