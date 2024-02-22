all done.

You can change option to use SQLlite
https://github.com/extrading/aCHCl4mI/blob/main/main.py#L75

Please notice. You have to deploy helm manifest before check task because I've used volumeClaimTemplates for file and database SQLlite to /app or use docker command like this:

`docker volume create my-vol`
`docker run -p 80:80 --mount source=my-vol,target=/app -d errbx/exness:latest`