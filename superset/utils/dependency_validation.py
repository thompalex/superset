# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Validate that pinned dependency versions match expectations."""

from __future__ import annotations

import logging
from importlib.metadata import version as get_version

from packaging.version import Version

logger = logging.getLogger(__name__)

# Expected version ranges for pinned dependencies
PINNED_DEPS: dict[str, tuple[str, str]] = {
    "cryptography": ("41.0.0", "42.0.0"),
    "Pillow": ("10.2.0", "11.0.0"),
    "Jinja2": ("3.1.6", "3.2.0"),
}


def validate_dependency_versions() -> None:
    """Raise ``RuntimeError`` if any pinned dependency is outside its range.

    Each entry in ``PINNED_DEPS`` maps a distribution name to a
    ``(min_inclusive, max_exclusive)`` version window.  The function
    logs a warning for every mismatch and raises after checking all
    entries so that operators see every problem at once.
    """
    errors: list[str] = []
    for dist_name, (min_ver, max_ver) in PINNED_DEPS.items():
        installed = Version(get_version(dist_name))
        low = Version(min_ver)
        high = Version(max_ver)
        if not (low <= installed < high):
            msg = (
                f"{dist_name}=={installed} is outside the expected "
                f"range [{min_ver}, {max_ver})"
            )
            logger.error(msg)
            errors.append(msg)
        else:
            logger.info(
                "%s==%s is within the expected range [%s, %s)",
                dist_name,
                installed,
                min_ver,
                max_ver,
            )

    if errors:
        raise RuntimeError("Dependency version check failed:\n  " + "\n  ".join(errors))
