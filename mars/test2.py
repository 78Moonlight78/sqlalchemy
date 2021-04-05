from requests import get, post

print(post('http://localhost:5000/api/jobs', 
           json={
                'id': 100,
                'job': 'Very important job',
                'work_size': 120,
                'collaborators': '2, 3, 4',
                'is_finished': False,
                'category': 2,
                'team_leader': 1
           }).json())
print(post('http://localhost:5000/api/jobs', 
           json={
                'id': 50,
                'job': 'Very important job',
                'work_size': 120,
                'collaborators': '2, 3, 4',
                'is_finished': False,
                'category': 2,
                'team_leader': 1
           }).json())
print(post('http://localhost:5000/api/jobs', 
           json={
                'job': 'Very important job',
                'work_size': 120,
                'collaborators': '2, 3, 4',
                'is_finished': False,
                'team_leader': 1
           }).json())
print(post('http://localhost:5000/api/jobs').json())


print(get('http://localhost:5000/api/jobs').json())