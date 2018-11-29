import requests

def import_gists_to_database(db, username, commit=True):
    r = requests.get('https://api.github.com/users/{}/gists'.format(username))
    r.raise_for_status()
    
    insert_query = '''
    INSERT INTO gists (
        "github_id", "html_url", "git_pull_url",
        "git_push_url", "commits_url",
        "forks_url", "public", "created_at",
        "updated_at", "comments", "comments_url"
    ) VALUES (
        :github_id, :html_url, :git_pull_url,
        :git_push_url, :commits_url, :forks_url,
        :public, :created_at, :updated_at,
        :comments, :comments_url
    );
    '''
    
    for gist in r.json():
        params = {
            "github_id": gist['id'],
            "html_url": gist['html_url'],
            "git_pull_url": gist['git_pull_url'],
            "git_push_url": gist['git_push_url'],
            "commits_url": gist['commits_url'],
            "forks_url": gist['forks_url'],
            "public": gist['public'],
            "created_at": gist['created_at'],
            "updated_at": gist['updated_at'],
            "comments": gist['comments'],
            "comments_url": gist['comments_url']
        }
        db.execute(insert_query, params)
    
    if commit:
        db.commit()
