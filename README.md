<p align="center">
  <a href="https://www.linkedin.com/in/zakharb/fuze">
  <img src="img/logo.png" alt="logo" />
</p>

<p align="center">

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&pause=1000&color=fff&center=true&width=500&lines=+AI+Ruleness+OT+SIEM;+Autonomous+ICS+protection;+Copilot+for+OT+SOC" alt="description" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1-white" height="20"/>
  <img src="https://img.shields.io/badge/python-3.11-white" height="20"/>
</p>


<p align="center">
  <img src="img/usage.gif" alt="usage" />
</p>


## :white_medium_square: Getting Started

[FUZE](https://github.com/zakharb/fuze) is an autonomous [OT SIEM](https://en.wikipedia.org/wiki/Security_information_and_event_management) tailored for ICS environments.

Leveraging AI to automatically collect Messages, normalize Events, and detect Incidents without the need for manual rule-writing.

Designed to enhance OT/ICS security and efficiency, FUZE offers advanced threat detection capabilities through its AI-driven approach, ensuring proactive defense in critical Industrial systems.


### Requirements

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

### Installing

Clone the project

```
git clone git@github.com:zakharb/fuze.git
cd fuze
```

Start docker-compose

```
docker-compose up --build --force --remove-orphans
```

<p align="center">
  <img src="img/install.gif" alt="animated" />
</p>

## :white_medium_square: Usage  


## :white_medium_square: Configuration  
Main configuration is `docker-compose.yml`  


## :white_medium_square: Deployment

Edit `Dockerfile` for each `Service` and deploy containers

## :white_medium_square: Versioning

Using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zakharb/fuze/tags). 

## :white_medium_square: Authors

* **Zakhar Bernhardt** - *Initial work* - [Ze](https://github.com/zakharb)

See also the list of [contributors](https://github.com/zakharb/fuze/contributors) who participated in this project.

## :white_medium_square: License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details
