import os
import shlex
import subprocess

import questionary

Q_STYLE = questionary.Style(
    [
        ("qmark", "fg:#FF0064 bold"),
        ("question", "fg:#00d1ff bold"),
        ("answer", "bold"),
        ("pointer", "fg:#8FFF00 bold"),
        ("highlighted", "fg:#8FFF00 bold"),
        ("selected", "fg:#cc5454"),
        ("separator", "fg:#cc5454"),
        ("instruction", "fg:#FBFFBC"),
        ("text", "fg:#DCFFF9"),
        ("disabled", "fg:#858585 italic"),
    ]
)


def invoke(cmd):
    """
    MIT License

    Copyright (c) 2020 Victor San Kho Lin

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT).decode()
        success = True
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        success = False
    return success, output.strip("\n")


def xu(path):
    """
    MIT License

    Copyright (c) 2020 Victor San Kho Lin

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    if str(path).startswith("~"):
        return os.path.expanduser(path)
    else:
        return path


def get_sso_profiles(config_file):
    """Get the list of SSO profiles from the AWS config file."""

    with open(xu(config_file), "r", encoding="utf-8") as file:
        lines = file.readlines()

    profiles = [
        profile.replace("[profile ", "").replace("]", "").strip()
        for profile in lines
        if profile.startswith("[profile")
    ]

    profiles.append("default")

    return profiles


def switch_profile(profile):
    # write the AWS_PROFILE ~/.aws_current_profile
    with open(xu("~/.aws_current_profile"), "w", encoding="utf-8") as file:
        file.write(f"export AWS_PROFILE={profile}\n")

    # source it in the ~/.zshrc file
    with open(xu("~/.zshrc"), "a+", encoding="utf-8") as file:
        file.seek(0)
        for line in file.readlines():
            if line.strip() == "source ~/.aws_current_profile":
                break
        else:
            file.write("\nsource ~/.aws_current_profile\n")
