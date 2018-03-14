FROM python:alpine

# environment variables
ENV UNTROUBLED_TIMEOUT=20 \
    UNTROUBLED_CACHE_PATH="/cache" \
    UNTROUBLED_STORE_PATH="/store" \
    UNTROUBLED_WAIT_TIME=3600 \
    UNTROUBLED_MONTHS=0

# label
LABEL description="Spamscope: Untroubled Spam Fetcher"

# install SpamScope
RUN set -ex; \
    mkdir -p ${UNTROUBLED_CACHE_PATH} ${UNTROUBLED_STORE_PATH}; \
    pip install untroubled-spam-fetcher; \
    apk add --no-cache p7zip;

ENTRYPOINT [ "untroubled-spam-fetcher" ]
CMD [ "-h" ]

# volumes
VOLUME [ "${UNTROUBLED_CACHE_PATH}" ]
VOLUME [ "${UNTROUBLED_STORE_PATH}" ]