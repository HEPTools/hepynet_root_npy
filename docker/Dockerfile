FROM sauerburger/pyroot3:v6.22.02

# install uproot
RUN pip3 install --upgrade pip && pip3 install uproot==4.0.0

RUN echo "source /opt/root/bin/thisroot.sh" >>/home/user/.bashrc

ENTRYPOINT export PYTHONPATH="${PYTHONPATH}:/work" && /bin/bash
