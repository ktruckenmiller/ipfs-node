# FROM alpine
# RUN wget -q https://github.com/ipfs/kubo/releases/download/v0.14.0/kubo_v0.14.0_linux-amd64.tar.gz && \
#     tar xf kubo_v0.14.0_linux-amd64.tar.gz && \
#     mv go-ipfs/ipfs /usr/local/bin && \
#     rm -rf go-ipfs kubo_v0.14.0_linux-amd64.tar.gz

FROM ipfs/kub # but in amd64