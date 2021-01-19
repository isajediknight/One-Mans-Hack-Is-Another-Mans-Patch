import json,requests
token = input("Token: ")
session = requests.Session()
session.auth = ('token',token.strip())
connection_validation = session.get('https://api.github.com/user')
if(int(connection_validation.status_code) == 200):
    api_pull = session.get('https://api.github.com/repos/monero-project/monero/pulls/'+str(731))
    my_data = json.loads(api_pull.text)
    print('\nPull Request Number:\t' + str(my_data['number']) if 'number' in my_data else 'Pull Request Number:\tNot Found')
    print('Closed Date:\t\t' + str(my_data['closed_at']) if 'closed_at' in my_data else 'Closed Date:\tNot Found')
    print('Commits:\t\t' + str(my_data['commits']) if 'commits' in my_data else 'Commits:\tNot Found')
    print('Merge Commit:\t\thttps://github.com/monero-project/monero/commit/' + str(my_data['merge_commit_sha']) if 'merge_commit_sha' in my_data else 'Merge Commit:\tNot Found')
else:
    print("Connection to Github API unsuccessful")
session.close()