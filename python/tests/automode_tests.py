import unittest
import mock
import sys
from automode import _get_server_prefix_modes, _is_able_to_mode
import automode

class FakeWeechat(object):
    def infolist_get(self, pointer):
        pass
    def infolist_string(self, pointer, string):
        pass
    def infolist_next(self):
        pass

class AutomodeTestcase(unittest.TestCase):
    def setUp(self):
        automode.weechat = mock.MagicMock(FakeWeechat)

    def test_get_prefix_chars(self):
        automode.weechat.infolist_get = mock.Mock(return_value="0xpointer")
        automode._get_server_prefix_modes.__get_prefix_modes = mock.Mock(return_value="ov")
        automode._get_server_prefix_modes.__get_prefix_chars = mock.Mock(return_value="@+")
        automode.weechat.infolist_free = mock.Mock()

        prefix_modes, prefix_chars = _get_server_prefix_modes("freenode")
        self.assertEquals(["o", "v"], prefix_modes)
        self.assertEquals(["@", "+"], prefix_chars)

    def test_no_prefixes_cant_do_anything(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=([], []))
        self.assertFalse(_is_able_to_mode("rfc_lol", "o", "v"))

    def test_op_is_above_voice(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["o", "v"], ["@", "+"]))
        self.assertTrue(_is_able_to_mode("freenode", "o", "v"))
        self.assertFalse(_is_able_to_mode("freenode", "v", "o"))

    def test_voice_cant_voice_others(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["o", "v"], ["@", "+"]))
        self.assertFalse(_is_able_to_mode("freenode", "v", "v"))

    def test_op_can_op_others(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["o", "v"], ["@", "+"]))
        self.assertTrue(_is_able_to_mode("freenode", "o", "o"))

    def test_funny_mix_of_modes(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["v", "o"], ["+", "@"]))
        self.assertTrue(_is_able_to_mode("rfc_lol", "v", "o"))
        self.assertTrue(_is_able_to_mode("rfc_lol", "v", "v"))
        self.assertTrue(_is_able_to_mode("rfc_lol", "o", "o"))

        # undocumented, just assuming!
        # http://www.irc.org/tech_docs/draft-brocklesby-irc-isupport-03.txt
        self.assertFalse(_is_able_to_mode("rfc_lol", "o", "v"))

    # place: PREFIX=(AaQqfohv).*~&!@%+

    # PREFIX=(aohv)!@%+   (shadowircd)
    def test_shadowircd_owner_give_owner(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "a", "a"))

    def test_shadowircd_owner_give_operator(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "a", "o"))

    def test_shadowircd_owner_give_halfop(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "a", "h"))

    def test_shadowircd_owner_give_voice(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "a", "v"))

    def test_shadowircd_operator_not_give_owner(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "o", "a"))

    def test_shadowircd_operator_give_operator(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "o", "o"))

    def test_shadowircd_operator_give_halfop(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "o", "h"))

    def test_shadowircd_operator_give_voice(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "o", "v"))

    def test_shadowircd_halfop_not_give_owner(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "h", "q"))

    def test_shadowircd_halfop_not_give_owner(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "h", "o"))

    def test_shadowircd_halfop_not_give_halfop(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "h", "h"))

    def test_shadowircd_halfop_give_voice(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertTrue(_is_able_to_mode("shadowircd", "h", "v"))

    def test_shadowircd_voice_not_give_owner(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "v", "a"))

    def test_shadowircd_voice_not_give_operator(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "v", "o"))

    def test_shadowircd_voice_not_give_halfop(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "v", "h"))

    def test_shadowircd_voice_not_give_voice(self):
        automode._get_server_prefix_modes = mock.Mock(return_value=(["a", "o", "h", "v"], ["!", "@", "%", "+"]))
        self.assertFalse(_is_able_to_mode("shadowircd", "v", "v"))

if __name__ == '__main__':
    unittest.main()
