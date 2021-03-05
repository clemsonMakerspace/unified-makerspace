"""
## AWS CDK Assets

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All types moved to @aws-cdk/core.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.data_type(
    jsii_type="@aws-cdk/assets.CopyOptions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
    },
)
class CopyOptions:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
        ignore_mode: typing.Optional[aws_cdk.core.IgnoreMode] = None,
    ) -> None:
        """(deprecated) Obtains applied when copying directories into the staging location.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '

        :deprecated: see ``core.CopyOptions``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        """
        result = self._values.get("exclude")
        return result

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        """(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :stability: deprecated
        """
        result = self._values.get("follow")
        return result

    @builtins.property
    def ignore_mode(self) -> typing.Optional[aws_cdk.core.IgnoreMode]:
        """(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        """
        result = self._values.get("ignore_mode")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CopyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/assets.FingerprintOptions",
    jsii_struct_bases=[CopyOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
    },
)
class FingerprintOptions(CopyOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
        ignore_mode: typing.Optional[aws_cdk.core.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Options related to calculating source hash.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content

        :deprecated: see ``core.FingerprintOptions``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        """
        result = self._values.get("exclude")
        return result

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        """(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :stability: deprecated
        """
        result = self._values.get("follow")
        return result

    @builtins.property
    def ignore_mode(self) -> typing.Optional[aws_cdk.core.IgnoreMode]:
        """(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        """
        result = self._values.get("ignore_mode")
        return result

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        """(deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: deprecated
        """
        result = self._values.get("extra_hash")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FingerprintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/assets.FollowMode")
class FollowMode(enum.Enum):
    """(deprecated) Symlink follow mode.

    :deprecated: see ``core.SymlinkFollowMode``

    :stability: deprecated
    """

    NEVER = "NEVER"
    """(deprecated) Never follow symlinks.

    :stability: deprecated
    """
    ALWAYS = "ALWAYS"
    """(deprecated) Materialize all symlinks, whether they are internal or external to the source directory.

    :stability: deprecated
    """
    EXTERNAL = "EXTERNAL"
    """(deprecated) Only follows symlinks that are external to the source directory.

    :stability: deprecated
    """
    BLOCK_EXTERNAL = "BLOCK_EXTERNAL"
    """(deprecated) Forbids source from having any symlinks pointing outside of the source tree.

    This is the safest mode of operation as it ensures that copy operations
    won't materialize files from the user's file system. Internal symlinks are
    not followed.

    If the copy operation runs into an external symlink, it will fail.

    :stability: deprecated
    """


@jsii.interface(jsii_type="@aws-cdk/assets.IAsset")
class IAsset(typing_extensions.Protocol):
    """(deprecated) Common interface for all assets.

    :deprecated: use ``core.IAsset``

    :stability: deprecated
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAssetProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        """(deprecated) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :stability: deprecated
        """
        ...


class _IAssetProxy:
    """(deprecated) Common interface for all assets.

    :deprecated: use ``core.IAsset``

    :stability: deprecated
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/assets.IAsset"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        """(deprecated) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :stability: deprecated
        """
        return jsii.get(self, "sourceHash")


class Staging(
    aws_cdk.core.AssetStaging,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/assets.Staging",
):
    """(deprecated) Deprecated.

    :deprecated: use ``core.AssetStaging``

    :stability: deprecated
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        source_path: builtins.str,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[FollowMode] = None,
        ignore_mode: typing.Optional[aws_cdk.core.IgnoreMode] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param source_path: (deprecated) Local file or directory to stage.
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '

        :stability: deprecated
        """
        props = StagingProps(
            source_path=source_path,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
        )

        jsii.create(Staging, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/assets.StagingProps",
    jsii_struct_bases=[FingerprintOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "source_path": "sourcePath",
    },
)
class StagingProps(FingerprintOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[FollowMode] = None,
        ignore_mode: typing.Optional[aws_cdk.core.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        source_path: builtins.str,
    ) -> None:
        """(deprecated) Deprecated.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param source_path: (deprecated) Local file or directory to stage.

        :deprecated: use ``core.AssetStagingProps``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "source_path": source_path,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        """
        result = self._values.get("exclude")
        return result

    @builtins.property
    def follow(self) -> typing.Optional[FollowMode]:
        """(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :stability: deprecated
        """
        result = self._values.get("follow")
        return result

    @builtins.property
    def ignore_mode(self) -> typing.Optional[aws_cdk.core.IgnoreMode]:
        """(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        """
        result = self._values.get("ignore_mode")
        return result

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        """(deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: deprecated
        """
        result = self._values.get("extra_hash")
        return result

    @builtins.property
    def source_path(self) -> builtins.str:
        """(deprecated) Local file or directory to stage.

        :stability: deprecated
        """
        result = self._values.get("source_path")
        assert result is not None, "Required property 'source_path' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StagingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CopyOptions",
    "FingerprintOptions",
    "FollowMode",
    "IAsset",
    "Staging",
    "StagingProps",
]

publication.publish()
