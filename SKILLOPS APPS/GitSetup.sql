-- 1. Create a secret to store your GitHub PAT
CREATE OR REPLACE SECRET my_github_secret
  TYPE = password
  USERNAME = 'mahamfs2703'
  PASSWORD = 'Mahamshahaan@2719';

-- 2. Create an API integration for GitHub
CREATE OR REPLACE API INTEGRATION my_github_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/mahamfs2703/')
  ALLOWED_AUTHENTICATION_SECRETS = (my_github_secret)
  ENABLED = true;

-- 3. Create a Git repository object
CREATE OR REPLACE GIT REPOSITORY my_git_repo
  API_INTEGRATION = my_github_integration
  GIT_CREDENTIALS = my_github_secret
  ORIGIN = 'https://github.com/mahamfs2703/SKILLOPS_APPS.git';