#!/usr/bin/env python
# coding=utf-8

"""
ola simple fader.

    simple fades between cues

    history:
        see git commits

    todo:
        ~ idea research
        ~ all fine :-)
"""


import sys
import os
import array

from configdict import ConfigDict
from olathreaded import OLAThread, OLAThread_States


version = """09.03.2016 12:57 stefan"""


##########################################
# globals


##########################################
# functions


##########################################
# classes


class OLAFader(OLAThread):
    """Class that extends on OLAThread and implements the fading function."""

    def __init__(self, config):
        """init fader things."""
        # super(OLAThread, self).__init__()
        OLAThread.__init__(self)

        self.config = config
        # print("config: {}".format(self.config))

        self.interval = self.config['system']['update_interval']

        self.universe = self.config['universe']['output']
        # self.channel_count = 512
        self.universe = self.config['universe']['channel_count']
        self.channels_out = array.array('B')
        self.channels_start = []
        self.channels_dif = []

        # self.channels = []
        for channel_index in range(0, self.channel_count):
            self.channels_out.append(0)
            self.channels_start.append(0)
            self.channels_dif.append(0)

    def ola_connected(self):
        """register receive callback and switch to running mode."""
        self.wrapper.AddEvent(self.update_interval, _calculate_step)
        # python3 syntax
        # super().ola_connected()
        # python2 syntax
        # super(OLAThread, self).ola_connected()
        # explicit call
        OLAThread.ola_connected(self)

    def _calculate_step(self):
        # register new event (for correct timing as first thing.)
        self.wrapper.AddEvent(self.update_interval, _calculate_step)
        if self.state is OLAFader_States.:
            pass
        # calculate
        # TODO
        for channel_index in range(0, self.channel_count):
            pass
        # send new frame.
        self.dmx_send_frame(
            self.config['universe']['output'],
            self.channels_out
        )

##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')

    # parse arguments
    filename = "playlist.json"
    # only use args after script name
    arg = sys.argv[1:]
    if not arg:
        print("using standard values.")
        print(" Allowed parameters:")
        print("   filename for config file       (default='playlist.json')")
        print("")
    else:
        filename = arg[0]
        # if len(arg) > 1:
        #     pixel_count = int(arg[1])
    # print parsed argument values
    print('''values:
        filename :{}
    '''.format(filename))

    default_config = {
        'system': {
            'update_interval': 30,
            '16bitMode': False,
        },
        'universe': {
            'output': 1,
            'channel_count': 50,
        },
        'playlist': {
            'playlist1': {
                'repeat': True,
                'cues': [
                    {
                        'fadetime': 5,
                        'channels': {
                            '1': 33,
                            '2': 0,
                            '3': 100,
                            '10': 255,
                        }
                    },
                    {
                        'fadetime': 3,
                        'channels': {
                            '1': 100,
                            '2': 2,
                            '3': 200,
                            '10': 0,
                        }
                    },
                    {
                        'fadetime': 2,
                        'channels': {
                            '1': 255,
                            '10': 20,
                        }
                    },
                ],
            },
            'playlist2': {
                'repeat': True,
                'cues': [
                    {
                        'fadetime': 5,
                        'channels': {
                            '1':     33,
                            '2':      0,
                            '3':  10000,
                            '10': 65535,
                        }
                    },
                    {
                        'fadetime': 3,
                        'channels': {
                            '1':  10000,
                            '2':      2,
                            '3':    200,
                            '10':     0,
                        }
                    },
                    {
                        'fadetime': 2,
                        'channels': {
                            '1':  65000,
                            '10':    20,
                        }
                    },
                ],
            },
        },
    }
    my_config = ConfigDict(default_config, filename)
    print("my_config.config: {}".format(my_config.config))

    my_fader = OLAFader(my_config.config)

    my_fader.start_ola()

    # wait for user to hit key.
    run = True
    while run:
        try:
            value = input(
                "\n\n" +
                42*'*' +
                "\nhit a key to start the playlist.\n" +
                "\nCtrl+C to stop OLAFader\n" +
                42*'*' +
                "\n\n"
            )
            if "p" in value:
                my_fader.start_playlist('playlist1')
        except KeyboardInterrupt:
            print("\nstop OLAFader.")
            run = false
        except Exception as e:
            print("\nerror: {}".format(e))
            run = false

    # blocks untill thread has joined.
    my_fader.stop_ola()

    # as last thing we save the current configuration.
    # print("\nwrite config.")
    # my_config.write_to_file()

    # ###########################################
