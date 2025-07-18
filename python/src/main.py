import os
import logging
from github import Github

class IssueProcessingAgent:
    def __init__(self, logger, github_client):
        self.logger = logger
        self.github_client = github_client

    def process_issue(self, issue_content, repository, issue_number):
        self.logger.info("Starting issue processing")

        # Analyze the issue
        analysis = self.analyze_issue(issue_content)

        # Generate a comment
        comment = self.generate_comment(analysis, issue_content)

        # Post the comment to GitHub
        self.post_comment(repository, issue_number, comment)
        
        return "Issue processed successfully"

    def analyze_issue(self, issue_content):
        self.logger.info("Analyzing issue content")
        analysis = {}

        content = issue_content.lower()

        # Determine issue type
        if any(keyword in content for keyword in ["bug", "error", "issue"]):
            analysis['type'] = "bug"
        elif any(keyword in content for keyword in ["feature", "enhancement", "request"]):
            analysis['type'] = "feature"
        else:
            analysis['type'] = "question"

        # Determine priority
        if any(keyword in content for keyword in ["urgent", "critical", "high"]):
            analysis['priority'] = "high"
        elif "low" in content or "minor" in content:
            analysis['priority'] = "low"
        else:
            analysis['priority'] = "medium"

        # Extract key topics
        topics = []
        if "tpm" in content:
            topics.append("TPM")
        if "security" in content:
            topics.append("Security")
        if "docker" in content:
            topics.append("Docker")

        analysis['topics'] = topics
        return analysis

    def generate_comment(self, analysis, issue_content):
        comment = "Thank you for this issue!\n\n"
        comment += "## Analysis Results\n\n"
        comment += f"- **Type**: {analysis['type']}\n"
        comment += f"- **Priority**: {analysis['priority']}\n"
        if analysis['topics']:
            comment += f"- **Topics**: {', '.join(analysis['topics'])}\n"
        return comment

    def post_comment(self, repository, issue_number, comment):
        owner, repo = repository.split('/')
        issue = self.github_client.get_repo(f"{owner}/{repo}").get_issue(number=issue_number)
        issue.create_comment(comment)
        issue.create_label(name="processed")
        self.logger.info("Comment posted successfully")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("AI Workflow Agent")

    # Read environment variables
    issue_content = os.getenv("INPUT_ISSUE_CONTENT", "")
    github_token = os.getenv("INPUT_GITHUB_TOKEN", "")
    repository = os.getenv("INPUT_REPOSITORY", "")
    issue_number = os.getenv("INPUT_ISSUE_NUMBER", "")

    if not all([issue_content, github_token, repository, issue_number]):
        logger.error("Missing required environment variables")
        exit(1)

    try:
        github_client = Github(github_token)
        agent = IssueProcessingAgent(logger, github_client)
        result = agent.process_issue(issue_content, repository, int(issue_number))
        logger.info(result)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        exit(1)
