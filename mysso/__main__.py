import questionary

from . import utils as u

DEFAULT_AWS_CONFIG_FILE = "~/.aws/config"


def main():
    profile = questionary.select(
        "Select a profile:", choices=u.get_sso_profiles(DEFAULT_AWS_CONFIG_FILE), style=u.Q_STYLE
    ).ask()

    if not profile:
        questionary.print("❌ No profile selected.", style="fg:#b031de bold italic")
        return

    questionary.print(f"\nChecking credentials validity for {profile} 🚀\n", style="fg:#b031de bold italic")

    sts_status, _ = u.invoke(f"aws sts get-caller-identity --profile {profile}")

    if sts_status:
        questionary.print(f"\nProfile '{profile}' still valid 🚀\n", style="fg:#b031de bold italic")

        u.switch_profile(profile)

        questionary.print(f"\nSwitched to {profile} 🚀\n", style="fg:#b031de bold italic")
        return

    questionary.print(f"\nCredentials for {profile} are invalid. Logging in... 🚀\n", style="fg:#b031de bold italic")

    sso_status, sso_output = u.invoke(f"aws sso login --profile {profile}")

    if not sso_status:
        questionary.print(f"🔥 {sso_output}", style="fg:#eb4034 bold italic")
        return

    u.switch_profile(profile)
    
    questionary.print("\nRefreshed sso credentials 🚀\n", style="fg:#b031de bold italic")


if __name__ == "__main__":
    main()
