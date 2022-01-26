# iotsim

IoT Simulator

어떤 IoT 사물이 센서들과 통신을 하여 데이터를 가져올 때,

센서의 데이터 송신 주기, 센서로부터 IoT 사물까지의 전송 속도, 데이터 계산 속도 등이

주어졌을 때, IoT 사물이 센서로부터 데이터를 가지고 결과값을 도출하는 것을

시뮬레이션 해보는 프로그램입니다.

사용자가 트리를 sparse matrix 형식으로 입력해주고 루트를 지정해주면,

주기적으로 데이터를 송신하는 leaf node 와, 이를 받아서 계산하여 부모 노드에게 보내주는 middle node(Internal node),

데이터를 받아서 계산이 끝났을 때 사용자에게 알려주는 root node 를 소켓으로 만들어서

루트까지 데이터가 왔을 때 메시지로 안내해주고, 이를 반복하는 프로그램입니다.

* 현재는 센서의 데이터 송신 주기만 구현하였습니다.
# 실행 방법
python main.py config_파일명 로 실행

예시) python main.py iotsim.conf

## confing 파일 파라미터들 설명

midnode_op 는 중간 노드들에서 어떤 오퍼레이션을 할건지 pass/average/max 의 3가지 옵션이 있고,

(자식 노드들의 데이터를 그대로 넘겨주기/ 자식 노드들의 데이터의 평균 값 념겨주기/ 자식 노드들의 데이터의 최댓값 넘겨주기), 

midnode_print 는 중간 노드들이 데이터를 보낼 때 화면에 출력 해줄 것인지, 

midnode_interval 은 중간 노드가 몇초 간격으로 데이터를 위로 전달해줄 것인지를 표현합니다.

input_form 은 어떤 형식으로 트리를 입력받을지 정해줍니다. 

1을 입력할 경우, 사용자가 따로 간선들을 다 지정해서 새로운 txt 파일 안에 넣어주고 그것을

iot_tree_structure_file 파라미터 안에 넣어 프로그램이 읽게 되고,

2를 입력할 경우 차수만 fan_out_degree 파라미터 안에 넣어주면

자동으로 해당 차수를 갖는 complete tree 가 생성됩니다.

### input_form 에 1을 입력해 iot_tree_structure_file 을 따로 만들 경우

첫번째 줄부터 N-1번째 줄까지 각 간선 정보를 **두 노드의 집합**으로 표현해줍니다.

(이 때 fan_out_degree 는 각 edges 정보를 수동으로 입력받기에, 어떤 값을 넣던 무시됩니다.)

ex) config 파일 [tree_info] 에 아래와 같이,

node_num:7

root_index:1

텍스트 파일안에 아래와 같이 입력시

1 2

1 3

2 4

2 5

3 6

3 7


아래와 같은 모양의 트리가 내부적으로 생성됩니다.

           1
       2       3
     4   5   6   7

### input_form 에 2을 입력했을 경우: 
[tree_info] 안에 있는 fan_out_degree 파라미터에 원하는 차수를 입력해주면,

자동으로 1번 노드를 루트로하는 complete 트리가 생성 됩니다.

(이 때 root_index 는 자동으로 1로 설정되기에, 어떤 값을 넣던 무시됩니다.)

ex) config 파일 [tree_info] 에 아래와 같이 입력시

node_num:7

root_index:1

fan_out_degree:2

역시 아래와 같은 모양의 트리가 내부적으로 생성됩니다.

           1
       2       3
     4   5   6   7

# 프로그램 실행 도중 가능한 명령어들
 - chmidop (max/average/pass): 중간 노드에서 수행하는 오퍼레이션을 일괄적으로 바꿔준다.
 - chmidintvl int: 중간 노드가 데이터를 보내는 인터벌을 바꿔준다.
 - chleafdata int int: leaf 노드가 보내는 데이터의 범위를 정해주어서, 해당 범위 내의 랜덤 데이터를 leaf 노드가 보낼 수 있게 해준다.
 - chleafintvl int: leaf 노드가 데이터를 보내는 인터벌을 바꿔준다.

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/bctak/iotsim.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://gitlab.com/bctak/iotsim/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!).  Thank you to [makeareadme.com](https://gitlab.com/-/experiment/new_project_readme_content:a504ea80101e2b52e983038a4f0a4586?https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

