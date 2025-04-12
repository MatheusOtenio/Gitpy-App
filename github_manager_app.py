import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
from github import Github
from typing import Optional
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import Image
import os
from github_api import GitHubAPI

class GitHubManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("GitHub Account Manager")
        self.geometry("1000x700")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize variables
        self.github_client: Optional[Github] = None
        self.github_api: Optional[GitHubAPI] = None
        self.current_user = None
        self._setup_variables()

        # Create sidebar
        self._create_sidebar()

        # Create main content area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Create tab views
        self._create_tabs()

        # Show authentication tab initially
        self._show_auth_tab()

    def _setup_variables(self):
        self.appearance_mode = ctk.StringVar(value="dark")
        self.current_tab = None
        self.stats_canvas = None

    def _create_sidebar(self):
        # Create sidebar frame
        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        sidebar.grid_propagate(False)

        # App title
        title = ctk.CTkLabel(sidebar, text="GitHub Manager", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)

        # Navigation buttons
        self.nav_buttons = {}
        for idx, (text, command) in enumerate([
            ("Authentication", self._show_auth_tab),
            ("Social", self._show_social_tab),
            ("Repositories", self._show_repos_tab),
            ("Statistics", self._show_stats_tab)
        ]):
            btn = ctk.CTkButton(sidebar, text=text, command=command)
            btn.pack(pady=5, padx=20, fill="x")
            self.nav_buttons[text] = btn

        # Appearance mode toggle
        mode_label = ctk.CTkLabel(sidebar, text="Appearance Mode:")
        mode_label.pack(pady=(20, 0))
        mode_switch = ctk.CTkOptionMenu(
            sidebar,
            values=["Light", "Dark"],
            command=self._change_appearance_mode,
            variable=self.appearance_mode
        )
        mode_switch.pack(pady=10)

    def _create_tabs(self):
        # Authentication tab content
        self.auth_frame = ctk.CTkFrame(self.main_frame)
        self._create_auth_content(self.auth_frame)

        # Social tab content
        self.social_frame = ctk.CTkFrame(self.main_frame)
        self._create_social_content(self.social_frame)

        # Repositories tab content
        self.repos_frame = ctk.CTkFrame(self.main_frame)
        self._create_repos_content(self.repos_frame)

        # Statistics tab content
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self._create_stats_content(self.stats_frame)

    def _create_auth_content(self, parent):
        # Token input
        token_label = ctk.CTkLabel(parent, text="GitHub Token:")
        token_label.pack(pady=(20, 5))
        self.token_entry = ctk.CTkEntry(parent, show="*", width=400)
        self.token_entry.pack(pady=(0, 20))

        # Authenticate button
        auth_button = ctk.CTkButton(
            parent,
            text="Authenticate",
            command=self.authenticate
        )
        auth_button.pack(pady=10)

        # Status label
        self.auth_status = ctk.CTkLabel(parent, text="")
        self.auth_status.pack(pady=10)

    def _create_social_content(self, parent):
        # Target username frame
        target_frame = ctk.CTkFrame(parent)
        target_frame.pack(fill="x", padx=20, pady=10)
        
        target_label = ctk.CTkLabel(target_frame, text="Target Username:")
        target_label.pack(side="left", padx=5)
        
        self.target_entry = ctk.CTkEntry(target_frame, width=200)
        self.target_entry.pack(side="left", padx=5)

        # Social actions frame
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=20, pady=10)

        # Action buttons
        ctk.CTkButton(actions_frame, text="Follow User", command=lambda: self._handle_social_action("follow")).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Unfollow User", command=lambda: self._handle_social_action("unfollow")).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="List Following", command=lambda: self._handle_social_action("following")).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="List Followers", command=lambda: self._handle_social_action("followers")).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Unfollow Non-followers", command=lambda: self._handle_social_action("unfollow_non_followers")).pack(side="left", padx=5)

        # Export frame
        export_frame = ctk.CTkFrame(parent)
        export_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(export_frame, text="Export as JSON", command=lambda: self._export_data("json")).pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="Export as CSV", command=lambda: self._export_data("csv")).pack(side="left", padx=5)

        # Output area
        self.social_output = ctk.CTkTextbox(parent, height=300)
        self.social_output.pack(fill="both", expand=True, padx=20, pady=10)

    def _create_repos_content(self, parent):
        # Search frame
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=20, pady=10)

        search_label = ctk.CTkLabel(search_frame, text="Search Repositories:")
        search_label.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(search_frame, width=200)
        self.search_entry.pack(side="left", padx=5)

        search_button = ctk.CTkButton(search_frame, text="Search", command=self._search_repos)
        search_button.pack(side="left", padx=5)

        # Repository actions frame
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(actions_frame, text="List Repositories", command=self._list_repos).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Create Repository", command=self._show_create_repo_dialog).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Delete Repository", command=self._show_delete_repo_dialog).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Toggle Visibility", command=self._show_toggle_visibility_dialog).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Clone Repository", command=self._show_clone_dialog).pack(side="left", padx=5)

        # Output area
        self.repos_output = ctk.CTkTextbox(parent, height=300)
        self.repos_output.pack(fill="both", expand=True, padx=20, pady=10)

    def _create_stats_content(self, parent):
        self.stats_frame = parent
        # Stats will be populated when showing the tab

    def _show_auth_tab(self):
        self._hide_current_tab()
        self.current_tab = self.auth_frame
        self.auth_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def _show_social_tab(self):
        if not self._check_auth(): return
        self._hide_current_tab()
        self.current_tab = self.social_frame
        self.social_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def _show_repos_tab(self):
        if not self._check_auth(): return
        self._hide_current_tab()
        self.current_tab = self.repos_frame
        self.repos_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def _show_stats_tab(self):
        if not self._check_auth(): return
        self._hide_current_tab()
        self.current_tab = self.stats_frame
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self._update_stats()

    def _hide_current_tab(self):
        if self.current_tab:
            self.current_tab.grid_remove()

    def _change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode.lower())

    def authenticate(self):
        token = self.token_entry.get()
        if not token:
            self._show_error("Please enter your GitHub token")
            return

        try:
            self.github_api = GitHubAPI(token)
            self.current_user = self.github_api.user.login
            self.auth_status.configure(
                text=f"Successfully authenticated as {self.current_user}",
                text_color="green"
            )
        except Exception as e:
            self._show_error(f"Authentication Error: {str(e)}")
            self.github_api = None
            self.current_user = None

    def _check_auth(self) -> bool:
        if not self.github_api:
            self._show_error("Please authenticate first")
            self._show_auth_tab()
            return False
        return True

    def _handle_social_action(self, action: str):
        if not self._check_auth(): return

        try:
            result = None
            if action == "follow":
                target = self.target_entry.get()
                if not target:
                    self._show_error("Please enter a target username")
                    return
                result = self.github_api.follow_user(target)
            elif action == "unfollow":
                target = self.target_entry.get()
                if not target:
                    self._show_error("Please enter a target username")
                    return
                result = self.github_api.unfollow_user(target)
            elif action == "following":
                result = {"status": "success", "data": self.github_api.get_following()}
            elif action == "followers":
                result = {"status": "success", "data": self.github_api.get_followers()}
            elif action == "unfollow_non_followers":
                result = self.github_api.unfollow_non_followers()

            self._update_social_output(result)
        except Exception as e:
            self._show_error(str(e))

    def _update_social_output(self, result: dict):
        if not result:
            return

        self.social_output.delete("1.0", tk.END)
        if result["status"] == "success":
            color = "green"
            if "data" in result:
                text = "\n".join(result["data"])
            elif "message" in result:
                text = result["message"]
            else:
                text = str(result)
        else:
            color = "red"
            text = result.get("message", str(result))

        self.social_output.insert("1.0", text)
        self.social_output.configure(text_color=color)

    def _show_error(self, message: str):
        self.social_output.delete("1.0", tk.END)
        self.social_output.insert("1.0", f"Error: {message}")
        self.social_output.configure(text_color="red")

    def _export_data(self, format: str):
        if not self._check_auth(): return

        try:
            data = {
                "followers": self.github_api.get_followers(),
                "following": self.github_api.get_following()
            }

            if format == "json":
                with open("github_data.json", "w") as f:
                    json.dump(data, f, indent=2)
                self._show_success("Data exported to github_data.json")
            else:  # CSV
                df = pd.DataFrame(data)
                df.to_csv("github_data.csv", index=False)
                self._show_success("Data exported to github_data.csv")
        except Exception as e:
            self._show_error(f"Export failed: {str(e)}")

    def _show_success(self, message: str):
        self.social_output.delete("1.0", tk.END)
        self.social_output.insert("1.0", message)
        self.social_output.configure(text_color="green")

    def _update_stats(self):
        if not self._check_auth(): return

        try:
            # Clear previous stats
            for widget in self.stats_frame.winfo_children():
                widget.destroy()

            # Get repository data
            repos = self.github_api.list_repositories()
            
            # Create figure for matplotlib
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            fig.patch.set_facecolor('none')

            # Visibility stats
            visibility_counts = {
                "public": sum(1 for r in repos if r["visibility"] == "public"),
                "private": sum(1 for r in repos if r["visibility"] == "private")
            }
            ax1.pie(
                visibility_counts.values(),
                labels=visibility_counts.keys(),
                autopct='%1.1f%%',
                colors=['lightblue', 'lightgreen']
            )
            ax1.set_title('Repository Visibility')

            # Repository count over time (placeholder for now)
            repos_count = len(repos)
            ax2.bar(['Total Repositories'], [repos_count], color='lightblue')
            ax2.set_title('Total Repositories')

            # Create canvas
            canvas = FigureCanvasTkAgg(fig, self.stats_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            plt.close(fig)  # Close the figure to free memory

        except Exception as e:
            self._show_error(f"Failed to update stats: {str(e)}")

    def _search_repos(self):
        if not self._check_auth(): return
        query = self.search_entry.get().lower()
        repos = self.github_api.list_repositories()
        
        filtered_repos = [repo for repo in repos if query in repo["name"].lower()]
        self._display_repos(filtered_repos)

    def _list_repos(self):
        if not self._check_auth(): return
        repos = self.github_api.list_repositories()
        self._display_repos(repos)

    def _display_repos(self, repos: list):
        self.repos_output.delete("1.0", tk.END)
        for repo in repos:
            self.repos_output.insert("end", f"Name: {repo['name']}\n")
            self.repos_output.insert("end", f"Description: {repo['description']}\n")
            self.repos_output.insert("end", f"Visibility: {repo['visibility']}\n")
            self.repos_output.insert("end", f"URL: {repo['url']}\n\n")

    def _show_create_repo_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter repository name:", title="Create Repository")
        name = dialog.get_input()
        if name:
            result = self.github_api.create_repository(name)
            self._display_repos([result])

    def _show_delete_repo_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter repository name to delete:", title="Delete Repository")
        name = dialog.get_input()
        if name:
            result = self.github_api.delete_repository(name)
            self._show_success(result["message"])

    def _show_toggle_visibility_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter repository name:", title="Toggle Visibility")
        name = dialog.get_input()
        if name:
            result = self.github_api.toggle_visibility(name)
            self._show_success(result["message"])

    def _show_clone_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter repository URL:", title="Clone Repository")
        url = dialog.get_input()
        if url:
            # Implement repository cloning logic here
            self._show_success(f"Repository cloning not implemented yet")

if __name__ == "__main__":
    app = GitHubManagerApp()
    app.mainloop()