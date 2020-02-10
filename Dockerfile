FROM continuumio/miniconda3
LABEL maintainer "Max Del Giudice <maxdelgiudice@gmail.com>"

# Create non-root user for our container
RUN useradd -ms /bin/bash url_shortener
RUN mkdir /home/url_shortener/web
WORKDIR /home/url_shortener

# Build conda environment (do this before other steps b/c it is time consuming)
COPY web/environment.yml ./web/environment.yml
RUN conda env create -f ./web/environment.yml

# Copy other files/folders to working directory, switch working directory
COPY web ./web
COPY .git ./web/.git
WORKDIR /home/url_shortener/web

# Make boot scripts executable
RUN chmod +x ./bin/boot_dev.sh ./bin/boot_prod.sh

# Switch user to non-root
RUN chown -R url_shortener:url_shortener ./
USER url_shortener

# Run program
EXPOSE 5000
ENTRYPOINT ["sh", "-c", "./bin/boot_${ENV}.sh"]
