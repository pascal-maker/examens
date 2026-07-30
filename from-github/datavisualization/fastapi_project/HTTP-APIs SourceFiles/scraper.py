import json
import requests

def get_html(url):
    r = requests.get(url)
    return r.json()

data = []

courses = [
    "https://www.mct.be/programma/basic-programming/index.json",
"https://www.mct.be/programma/frontend-foundations/index.json",
"https://www.mct.be/programma/user-experience-design/index.json",
"https://www.mct.be/programma/computer-networks/index.json",
"https://www.mct.be/programma/data-science/index.json",
"https://www.mct.be/programma/prototyping/index.json",
"https://www.mct.be/programma/full-stack-web-development/index.json",
"https://www.mct.be/programma/user-interface-design/index.json",
"https://www.mct.be/programma/sensors-interfacing/index.json",
"https://www.mct.be/programma/datamanagement/index.json",
"https://www.mct.be/programma/project-one/index.json",
"https://www.mct.be/programma/device-programming/index.json",
"https://www.mct.be/programma/interaction-design/index.json",
"https://www.mct.be/programma/security/index.json",
"https://www.mct.be/programma/iot-cloud/index.json",
"https://www.mct.be/programma/team-project/index.json",
"https://www.mct.be/programma/backend-development/index.json",
"https://www.mct.be/programma/frontend-development/index.json",
"https://www.mct.be/programma/network-infrastructure/index.json",
"https://www.mct.be/programma/unity/index.json",
"https://www.mct.be/programma/3d1/index.json",
"https://www.mct.be/programma/advanced-programming-maths/index.json",
"https://www.mct.be/programma/big-data/index.json",
"https://www.mct.be/programma/linux-os/index.json",
"https://www.mct.be/programma/smart-app-development/index.json",
"https://www.mct.be/programma/virtualisation-cloud-computing-infrastructure/index.json",
"https://www.mct.be/programma/3d-rigging/index.json",
"https://www.mct.be/programma/applied-ai/index.json",
"https://www.mct.be/programma/machine-learning/index.json",
"https://www.mct.be/programma/motion-design/index.json",
"https://www.mct.be/programma/windows-os/index.json",
"https://www.mct.be/programma/industry-project/index.json",
"https://www.mct.be/programma/cloud-services/index.json",
"https://www.mct.be/programma/experimental-xr/index.json",
"https://www.mct.be/programma/future-technologies/index.json",
"https://www.mct.be/programma/mlops/index.json",
"https://www.mct.be/programma/advanced-full-stack-development/index.json",
"https://www.mct.be/programma/deep-learning/index.json",
"https://www.mct.be/programma/network-scripting/index.json",
"https://www.mct.be/programma/advanced-ai/index.json",
"https://www.mct.be/programma/mixed-reality/index.json",
"https://www.mct.be/programma/new-interface-design/index.json",
"https://www.mct.be/programma/iot-devices-robotics/index.json",
"https://www.mct.be/programma/the-collective/index.json",
"https://www.mct.be/programma/research-project/index.json",
"https://www.mct.be/programma/stage/index.json",
"https://www.mct.be/programma/bachelorproef/index.json",
]

# Store data in memory
for course in courses:
    data.append(get_html(course))

# Store data in file
with open('data.json', 'w') as f:
    json.dump(data, f)
