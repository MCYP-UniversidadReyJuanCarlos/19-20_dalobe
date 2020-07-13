# SDS project
[![python-app Actions Status](https://github.com/MCYP-UniversidadReyJuanCarlos/19-20_dalobe/workflows/python-app/badge.svg)](https://github.com/MCYP-UniversidadReyJuanCarlos/19-20_dalobe/actions)
[![python-app Actions Status](https://github.com/MCYP-UniversidadReyJuanCarlos/19-20_dalobe/coverage-badge.svg)](https://github.com/MCYP-UniversidadReyJuanCarlos/19-20_dalobe/htmlcov/index.html)


SDS is a tool to detect and implement security best practices over docker containers and images.
The scan can be performed by two ways:
- Dynamic analysis. In this approach, docker containers are scanned looking for potential security issues
by highlighting corrections needed to take into account as well as providing best practices 
for hardening your containers environment. The output is a report with the vulnerabilities found and a proposal
Dockerfile.
- Static analysis. Application can scan in an static way with a Dockerfile as an input. By this way,
the output is a report with the vulnerabilities found and a proposal Dockerfile.
Most of the best practices implemented are based on CIS Docker Benchmark document. To obtain the latest version of this guide, please
visit http://benchmarks.cisecurity.org.

## Built With 🛠️

![cover image](resources/docker_python_flask.png)
* [Docker SDK](https://docker-py.readthedocs.io/en/stable/) - Docker SDK for Python
* [Python](https://www.python.org/) - Python
* [Flask](https://www.fullstackpython.com/flask.html) - Python web framework

## Architecture 🛠️

![cover image](resources/SDS_architecture.png)

## Contributing 🖇️

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning 📌

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Change Log 📌

[CHANGELOG.md](CHANGELOG.md) for details

## Author ✒️

* **David López Beltrán** - *Initial work* - [dlpezbel](https://github.com/dlpezbel)

## License 📄

The code in this repository, including all code samples in the notebooks listed above, 
is released under the MIT license. Read more at the [LICENSE.md](LICENSE.md) for details.




