from bitmovin.errors import InvalidTypeError
from bitmovin.resources.enums import AACChannelLayout, HeAacSignaling
from bitmovin.utils import Serializable
from .audio_codec_configuration import AudioCodecConfiguration


class HeAACv1CodecConfiguration(AudioCodecConfiguration, Serializable):

    def __init__(self, name, bitrate, rate=None, id_=None, description=None, custom_data=None, channel_layout=None,
                 volume_adjust=None, normalize=None, signaling=None):

        super().__init__(id_=id_, name=name, bitrate=bitrate, rate=rate, description=description,
                         custom_data=custom_data)

        self.volumeAdjust = volume_adjust
        self.normalize = normalize

        self._channelLayout = None
        self.channelLayout = channel_layout

        self._signaling = None
        self.signaling = signaling

    @property
    def signaling(self):
        return self._signaling

    @signaling.setter
    def signaling(self, new_signaling):
        if new_signaling is None:
            self._signaling = None
            return
        if isinstance(new_signaling, str):
            self._signaling = new_signaling
        elif isinstance(new_signaling, HeAacSignaling):
            self._signaling = new_signaling.value
        else:
            raise InvalidTypeError(
                'Invalid type {} for signalling: must be either str or HeAacCodecConfigSignaling'.format(
                    type(new_signaling)))

    @property
    def channelLayout(self):
        return self._channelLayout

    @channelLayout.setter
    def channelLayout(self, new_layout):
        if new_layout is None:
            self._channelLayout = None
            return
        if isinstance(new_layout, str):
            self._channelLayout = new_layout
        elif isinstance(new_layout, AACChannelLayout):
            self._channelLayout = new_layout.value
        else:
            raise InvalidTypeError(
                'Invalid type {} for channelLayout: must be either str or AACChannelLayout!'.format(type(new_layout)))

    @classmethod
    def parse_from_json_object(cls, json_object):
        audio_codec_configuration = AudioCodecConfiguration.parse_from_json_object(json_object=json_object)
        id_ = audio_codec_configuration.id
        name = audio_codec_configuration.name
        description = audio_codec_configuration.description
        custom_data = audio_codec_configuration.customData

        bitrate = json_object['bitrate']

        rate = json_object.get('rate')
        channel_layout = json_object.get('channelLayout')
        volume_adjust = json_object.get('volumeAdjust')
        normalize = json_object.get('normalize')
        signaling = json_object.get('signaling')

        audio_codec_configuration = HeAACv1CodecConfiguration(id_=id_, name=name, description=description,
                                                              custom_data=custom_data, bitrate=bitrate, rate=rate,
                                                              channel_layout=channel_layout,
                                                              volume_adjust=volume_adjust,
                                                              normalize=normalize, signaling=signaling)

        return audio_codec_configuration

    def serialize(self):
        serialized = super().serialize()
        serialized['channelLayout'] = self.channelLayout
        serialized['signaling'] = self.signaling

        return serialized
