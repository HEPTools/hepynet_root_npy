FROM sauerburger/pyroot3:v6.22.02

# install uproot
USER root

RUN pip3 install --upgrade pip && pip3 install uproot==4.0.0

RUN echo "source /opt/root/bin/thisroot.sh" >> ~/.bashrc

ENTRYPOINT export PYTHONPATH="${PYTHONPATH}:/work" && /bin/bash
