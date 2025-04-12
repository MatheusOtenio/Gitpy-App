from github import Github
from github.GithubException import GithubException
from typing import List, Dict, Optional

class GitHubAPI:
    def __init__(self, token: str):
        self.client = Github(token)
        self.user = self.client.get_user()

    def follow_user(self, username: str) -> Dict[str, str]:
        """Follow a GitHub user."""
        try:
            target_user = self.client.get_user(username)
            self.user.add_to_following(target_user)
            return {"status": "success", "message": f"Successfully followed {username}"}
        except GithubException as e:
            return {"status": "error", "message": str(e)}

    def unfollow_user(self, username: str) -> Dict[str, str]:
        """Unfollow a GitHub user."""
        try:
            target_user = self.client.get_user(username)
            self.user.remove_from_following(target_user)
            return {"status": "success", "message": f"Successfully unfollowed {username}"}
        except GithubException as e:
            return {"status": "error", "message": str(e)}

    def get_following(self, username: Optional[str] = None) -> List[str]:
        """Get list of users being followed."""
        try:
            target = self.client.get_user(username) if username else self.user
            return [user.login for user in target.get_following()]
        except GithubException as e:
            return [f"Error: {str(e)}"]

    def get_followers(self, username: Optional[str] = None) -> List[str]:
        """Get list of followers."""
        try:
            target = self.client.get_user(username) if username else self.user
            return [user.login for user in target.get_followers()]
        except GithubException as e:
            return [f"Error: {str(e)}"]

    def unfollow_non_followers(self) -> Dict[str, List[str]]:
        """Unfollow users who don't follow back."""
        try:
            following = set(self.get_following())
            followers = set(self.get_followers())
            non_followers = following - followers
            
            unfollowed = []
            for username in non_followers:
                result = self.unfollow_user(username)
                if result["status"] == "success":
                    unfollowed.append(username)

            return {
                "status": "success",
                "unfollowed": unfollowed,
                "count": len(unfollowed)
            }
        except Exception as e:
            return {"status": "error", "unfollowed": [], "message": str(e)}

    def list_repositories(self, username: Optional[str] = None) -> List[Dict[str, str]]:
        """List repositories for a user."""
        try:
            target = self.client.get_user(username) if username else self.user
            repos = []
            for repo in target.get_repos():
                repos.append({
                    "name": repo.name,
                    "description": repo.description or "",
                    "visibility": "private" if repo.private else "public",
                    "url": repo.html_url
                })
            return repos
        except GithubException as e:
            return [{"error": str(e)}]

    def create_repository(self, name: str, description: str = "", private: bool = False) -> Dict[str, str]:
        """Create a new repository."""
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private
            )
            return {
                "status": "success",
                "message": f"Repository created successfully",
                "url": repo.html_url
            }
        except GithubException as e:
            return {"status": "error", "message": str(e)}

    def delete_repository(self, name: str) -> Dict[str, str]:
        """Delete a repository."""
        try:
            repo = self.user.get_repo(name)
            repo.delete()
            return {"status": "success", "message": f"Repository {name} deleted successfully"}
        except GithubException as e:
            return {"status": "error", "message": str(e)}

    def toggle_visibility(self, name: str) -> Dict[str, str]:
        """Toggle repository visibility between public and private."""
        try:
            repo = self.user.get_repo(name)
            new_visibility = not repo.private
            repo.edit(private=new_visibility)
            status = "private" if new_visibility else "public"
            return {
                "status": "success",
                "message": f"Repository {name} is now {status}"
            }
        except GithubException as e:
            return {"status": "error", "message": str(e)}