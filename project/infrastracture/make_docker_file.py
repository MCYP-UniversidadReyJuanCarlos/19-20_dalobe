

class Make_docker_file:

    def write_docker_file(container,fixes):
        image = container.image
        f = open('../../output/Dockerfile', mode='wt', encoding='utf-8')
        f.write("FROM " + str(image.attrs.get('RepoTags')[0]) + "\n\n")
        f.write(fixes)
        f.close()