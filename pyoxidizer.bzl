def make_dist():
    return default_python_distribution()

def make_packaging_policy(dist):
    policy = dist.make_python_packaging_policy()
    policy.set_resource_handling_mode("files")
    policy.resources_location = "filesystem-relative:ftt"
    policy.allow_files = True
    policy.bytecode_optimize_level_zero = True

    return policy

def make_client(dist, policy):
    python_config = dist.make_python_interpreter_config()
    python_config.module_search_paths = ["$ORIGIN", "$ORIGIN/ftt"]
    python_config.filesystem_importer = True
    python_config.sys_frozen = True
    python_config.run_command = "poetry install"
    python_config.run_command = "import ftt; from ftt.cli.shell import Shell; Shell.initialize_and_run()"

    ftt = dist.to_python_executable(
        name="fttcli",
        packaging_policy=policy,
        config=python_config,
    )
    # ibapi = PythonPackageDistributionResource("ibapi")
    # ibapi.add_include = True
    # ibapi.add_source('vendors/pythonclient')
    #
    # ftt.add_python_resources([ibapi])
    ftt.add_python_resources(ftt.pip_install(["--prefer-binary", "-r", "requirements.txt"]))

    return ftt

def make_embedded_resources(client):
    return client.to_embedded_resources()

def make_install(client, resources):
    files = FileManifest()
    files.add_python_resource(".", client)

    # static_resources = glob(["./*.py", "./*.md", "./*txt", "./static/**/*", "./help/**/*"], strip_prefix="{}/".format(CWD))
    # files.add_manifest(static_resources)

    ftt_source = glob(["./ftt/**/*.py"], strip_prefix="{}/".format(CWD))
    files.add_manifest(ftt_source)

    return files


# Call our function to set up automatic code signers.
register_target("dist", make_dist)
register_target("policy", make_packaging_policy, depends=["dist"])
register_target("client", make_client, depends=["dist", "policy"])
register_target("resources", make_embedded_resources, depends=["client"], default_build_script=True)
register_target("install", make_install, depends=["client", "resources"], default=True)

# Resolve whatever targets the invoker of this configuration file is requesting
# be resolved.
resolve_targets()
