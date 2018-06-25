# -*- coding: utf-8 -*-
'''
    :codeauthor: Jayesh Kariya <jayeshk@saltstack.com>
'''
# pylint: disable=3rd-party-module-not-gated

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals
import tempfile
import shutil

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.paths import TMP
from tests.support.unit import skipIf, TestCase
from tests.support.mock import (
    NO_MOCK,
    NO_MOCK_REASON,
    MagicMock,
    mock_open,
    patch)

# Import Salt Libs
import salt.states.virt as virt
import salt.utils.files


class LibvirtMock(MagicMock):  # pylint: disable=too-many-ancestors
    '''
    libvirt library mockup
    '''

    class libvirtError(Exception):  # pylint: disable=invalid-name
        '''
        libvirt error mockup
        '''


@skipIf(NO_MOCK, NO_MOCK_REASON)
class LibvirtTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.states.libvirt
    '''
    def setup_loader_modules(self):
        self.mock_libvirt = LibvirtMock()  # pylint: disable=attribute-defined-outside-init
        self.addCleanup(delattr, self, 'mock_libvirt')
        loader_globals = {
            'libvirt': self.mock_libvirt
        }
        return {virt: loader_globals}

    @classmethod
    def setUpClass(cls):
        cls.pki_dir = tempfile.mkdtemp(dir=TMP)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.pki_dir)
        del cls.pki_dir

    # 'keys' function tests: 1

    def test_keys(self):
        '''
        Test to manage libvirt keys.
        '''
        with patch('os.path.isfile', MagicMock(return_value=False)):
            name = 'sunrise'

            ret = {'name': name,
                   'result': True,
                   'comment': '',
                   'changes': {}}

            mock = MagicMock(side_effect=[[], ['libvirt.servercert.pem'],
                                          {'libvirt.servercert.pem': 'A'}])
            with patch.dict(virt.__salt__, {'pillar.ext': mock}):  # pylint: disable=no-member
                comt = ('All keys are correct')
                ret.update({'comment': comt})
                self.assertDictEqual(virt.keys(name, basepath=self.pki_dir), ret)

                with patch.dict(virt.__opts__, {'test': True}):  # pylint: disable=no-member
                    comt = ('Libvirt keys are set to be updated')
                    ret.update({'comment': comt, 'result': None})
                    self.assertDictEqual(virt.keys(name, basepath=self.pki_dir), ret)

                with patch.dict(virt.__opts__, {'test': False}):  # pylint: disable=no-member
                    with patch.object(salt.utils.files, 'fopen', MagicMock(mock_open())):
                        comt = ('Updated libvirt certs and keys')
                        ret.update({'comment': comt, 'result': True,
                                    'changes': {'servercert': 'new'}})
                        self.assertDictEqual(virt.keys(name, basepath=self.pki_dir), ret)

    def test_keys_with_expiration_days(self):
        '''
        Test to manage libvirt keys.
        '''
        with patch('os.path.isfile', MagicMock(return_value=False)):
            name = 'sunrise'

            ret = {'name': name,
                   'result': True,
                   'comment': '',
                   'changes': {}}

            mock = MagicMock(side_effect=[[], ['libvirt.servercert.pem'],
                                          {'libvirt.servercert.pem': 'A'}])
            with patch.dict(virt.__salt__, {'pillar.ext': mock}):  # pylint: disable=no-member
                comt = ('All keys are correct')
                ret.update({'comment': comt})
                self.assertDictEqual(virt.keys(name,
                                               basepath=self.pki_dir,
                                               expiration_days=700), ret)

                with patch.dict(virt.__opts__, {'test': True}):  # pylint: disable=no-member
                    comt = ('Libvirt keys are set to be updated')
                    ret.update({'comment': comt, 'result': None})
                    self.assertDictEqual(virt.keys(name,
                                                   basepath=self.pki_dir,
                                                   expiration_days=700), ret)

                with patch.dict(virt.__opts__, {'test': False}):  # pylint: disable=no-member
                    with patch.object(salt.utils.files, 'fopen', MagicMock(mock_open())):
                        comt = ('Updated libvirt certs and keys')
                        ret.update({'comment': comt, 'result': True,
                                    'changes': {'servercert': 'new'}})
                        self.assertDictEqual(virt.keys(name,
                                                       basepath=self.pki_dir,
                                                       expiration_days=700), ret)

    def test_keys_with_state(self):
        '''
        Test to manage libvirt keys.
        '''
        with patch('os.path.isfile', MagicMock(return_value=False)):
            name = 'sunrise'

            ret = {'name': name,
                   'result': True,
                   'comment': '',
                   'changes': {}}

            mock = MagicMock(side_effect=[[], ['libvirt.servercert.pem'],
                                          {'libvirt.servercert.pem': 'A'}])
            with patch.dict(virt.__salt__, {'pillar.ext': mock}):  # pylint: disable=no-member
                comt = ('All keys are correct')
                ret.update({'comment': comt})
                self.assertDictEqual(virt.keys(name,
                                               basepath=self.pki_dir,
                                               st='California'), ret)

                with patch.dict(virt.__opts__, {'test': True}):  # pylint: disable=no-member
                    comt = ('Libvirt keys are set to be updated')
                    ret.update({'comment': comt, 'result': None})
                    self.assertDictEqual(virt.keys(name,
                                                   basepath=self.pki_dir,
                                                   st='California'), ret)

                with patch.dict(virt.__opts__, {'test': False}):  # pylint: disable=no-member
                    with patch.object(salt.utils.files, 'fopen', MagicMock(mock_open())):
                        comt = ('Updated libvirt certs and keys')
                        ret.update({'comment': comt, 'result': True,
                                    'changes': {'servercert': 'new'}})
                        self.assertDictEqual(virt.keys(name,
                                                       basepath=self.pki_dir,
                                                       st='California'), ret)

    def test_keys_with_all_options(self):
        '''
        Test to manage libvirt keys.
        '''
        with patch('os.path.isfile', MagicMock(return_value=False)):
            name = 'sunrise'

            ret = {'name': name,
                   'result': True,
                   'comment': '',
                   'changes': {}}

            mock = MagicMock(side_effect=[[], ['libvirt.servercert.pem'],
                                          {'libvirt.servercert.pem': 'A'}])
            with patch.dict(virt.__salt__, {'pillar.ext': mock}):  # pylint: disable=no-member
                comt = ('All keys are correct')
                ret.update({'comment': comt})
                self.assertDictEqual(virt.keys(name,
                                               basepath=self.pki_dir,
                                               country='USA',
                                               st='California',
                                               locality='Los_Angeles',
                                               organization='SaltStack',
                                               expiration_days=700), ret)

                with patch.dict(virt.__opts__, {'test': True}):  # pylint: disable=no-member
                    comt = ('Libvirt keys are set to be updated')
                    ret.update({'comment': comt, 'result': None})
                    self.assertDictEqual(virt.keys(name,
                                                   basepath=self.pki_dir,
                                                   country='USA',
                                                   st='California',
                                                   locality='Los_Angeles',
                                                   organization='SaltStack',
                                                   expiration_days=700), ret)

                with patch.dict(virt.__opts__, {'test': False}):  # pylint: disable=no-member
                    with patch.object(salt.utils.files, 'fopen', MagicMock(mock_open())):
                        comt = ('Updated libvirt certs and keys')
                        ret.update({'comment': comt, 'result': True,
                                    'changes': {'servercert': 'new'}})
                        self.assertDictEqual(virt.keys(name,
                                                       basepath=self.pki_dir,
                                                       country='USA',
                                                       st='California',
                                                       locality='Los_Angeles',
                                                       organization='SaltStack',
                                                       expiration_days=700), ret)

    def test_running(self):
        '''
        running state test cases.
        '''
        ret = {'name': 'myvm',
               'changes': {},
               'result': True,
               'comment': 'myvm is running'}
        with patch.dict(virt.__salt__, {  # pylint: disable=no-member
                    'virt.vm_state': MagicMock(return_value='stopped'),
                    'virt.start': MagicMock(return_value=0)
                }):
            ret.update({'changes': {'myvm': 'Domain started'},
                        'comment': 'Domain myvm started'})
            self.assertDictEqual(virt.running('myvm'), ret)

        with patch.dict(virt.__salt__, {  # pylint: disable=no-member
                    'virt.vm_state': MagicMock(return_value='stopped'),
                    'virt.start': MagicMock(side_effect=[self.mock_libvirt.libvirtError('libvirt error msg')])
                }):
            ret.update({'changes': {}, 'result': False, 'comment': 'libvirt error msg'})
            self.assertDictEqual(virt.running('myvm'), ret)
