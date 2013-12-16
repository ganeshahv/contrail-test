from time import sleep

class VerifyEvpnCases():

    def verify_ipv6_ping_for_non_ip_communication(self,encap):

        # Setting up default encapsulation 
        self.logger.info('Deleting any Encap before continuing')
        out=self.connections.delete_vrouter_encap()
        self.logger.info('Setting new Encap before continuing')
        if (encap == 'gre'):
            config_id=self.connections.set_vrouter_config_encap('MPLSoGRE','MPLSoUDP','VXLAN')
            self.logger.info('Created.UUID is %s. MPLSoGRE is the highest priority encap'%(config_id))
        elif (encap == 'udp'): 
            config_id=self.connections.set_vrouter_config_encap('MPLSoUDP','MPLSoGRE','VXLAN')
            self.logger.info('Created.UUID is %s. MPLSoUDP is the highest priority encap'%(config_id))
        elif (encap == 'vxlan'):
            config_id=self.connections.set_vrouter_config_encap('VXLAN','MPLSoUDP','MPLSoGRE')
            self.logger.info('Created.UUID is %s. VXLAN is the highest priority encap'%(config_id))
          
        vn1_fixture= self.res.vn1_fixture
        vn2_fixture= self.res.vn2_fixture
        vn1_vm1_fixture= self.res.vn1_vm1_fixture
        vn1_vm2_fixture= self.res.vn1_vm2_fixture
        vm1_name= self.res.vn1_vm1_name
        vm2_name= self.res.vn1_vm2_name
        vn1_name= self.res.vn1_name
        vn1_subnets= self.res.vn1_subnets
        assert vn1_fixture.verify_on_setup()
        assert vn2_fixture.verify_on_setup()
        assert vn1_vm1_fixture.verify_on_setup()
        assert vn1_vm2_fixture.verify_on_setup()
        sleep(10)
        vm1_ipv6=vn1_vm1_fixture.get_vm_ipv6_addr_from_vm()
        vm2_ipv6=vn1_vm2_fixture.get_vm_ipv6_addr_from_vm()
        assert vn1_vm1_fixture.ping_to_ipv6(vm2_ipv6.split("/")[0],return_output=True)
        return True
    # End verify_ipv6_ping_for_non_ip_communication

    def verify_ping_to_configured_ipv6_address (self,encap):
        '''Configure IPV6 address to VM. Test IPv6 ping to that address.
        '''
        result= True
        # Setting up default encapsulation 
        self.logger.info('Deleting any Encap before continuing')
        out=self.connections.delete_vrouter_encap()
        self.logger.info('Setting new Encap before continuing')
        if (encap == 'gre'):
            config_id=self.connections.set_vrouter_config_encap('MPLSoGRE','MPLSoUDP','VXLAN')
            self.logger.info('Created.UUID is %s. MPLSoGRE is the highest priority encap'%(config_id))
        elif (encap == 'udp'):
            config_id=self.connections.set_vrouter_config_encap('MPLSoUDP','MPLSoGRE','VXLAN')
            self.logger.info('Created.UUID is %s. MPLSoUDP is the highest priority encap'%(config_id))
        elif (encap == 'vxlan'):
            config_id=self.connections.set_vrouter_config_encap('VXLAN','MPLSoUDP','MPLSoGRE')
            self.logger.info('Created.UUID is %s. VXLAN is the highest priority encap'%(config_id))

        vn1_vm1= '1001::1/64'
        vn1_vm2= '1001::2/64'
        vn1_fixture= self.res.vn1_fixture
        vn2_fixture= self.res.vn2_fixture
        vn1_vm1_fixture= self.res.vn1_vm1_fixture
        vn1_vm2_fixture= self.res.vn1_vm2_fixture
        vm1_name= self.res.vn1_vm1_name
        vm2_name= self.res.vn1_vm2_name
        vn1_name= self.res.vn1_name
        vn1_subnets= self.res.vn1_subnets
        assert vn1_fixture.verify_on_setup()
        assert vn2_fixture.verify_on_setup()  
        assert vn1_vm1_fixture.verify_on_setup()
        assert vn1_vm2_fixture.verify_on_setup()
        cmd_to_pass1=['ifconfig eth0 inet6 add %s' %(vn1_vm1)]
        vn1_vm1_fixture.run_cmd_on_vm(cmds=cmd_to_pass1)
        cmd_to_pass2=['ifconfig eth0 inet6 add %s' %(vn1_vm2)]
        vn1_vm2_fixture.run_cmd_on_vm(cmds=cmd_to_pass2)
        vm1_ipv6=vn1_vm1_fixture.get_vm_ipv6_addr_from_vm(addr_type='global')
        vm2_ipv6=vn1_vm2_fixture.get_vm_ipv6_addr_from_vm(addr_type='global')
        assert vn1_vm1_fixture.ping_to_ipv6(vm2_ipv6.split("/")[0],return_output=True)
        return True
    # End verify_ping_to_configured_ipv6_address

    def verify_epvn_with_agent_restart (self,encap):
        '''Restart the vrouter service and verify the impact on L2 route
        '''

        # Setting up default encapsulation 
        self.logger.info('Deleting any Encap before continuing')
        out=self.connections.delete_vrouter_encap()
        self.logger.info('Setting new Encap before continuing')
        if (encap == 'gre'):
            config_id=self.connections.set_vrouter_config_encap('MPLSoGRE','MPLSoUDP','VXLAN')
            self.logger.info('Created.UUID is %s. MPLSoGRE is the highest priority encap'%(config_id))
        elif (encap == 'udp'):
            config_id=self.connections.set_vrouter_config_encap('MPLSoUDP','MPLSoGRE','VXLAN')
            self.logger.info('Created.UUID is %s. MPLSoUDP is the highest priority encap'%(config_id))
        elif (encap == 'vxlan'):
            config_id=self.connections.set_vrouter_config_encap('VXLAN','MPLSoUDP','MPLSoGRE')
            self.logger.info('Created.UUID is %s. VXLAN is the highest priority encap'%(config_id))

        result= True
        vn1_fixture= self.res.vn1_fixture
        vn2_fixture= self.res.vn2_fixture
        vn1_vm1_fixture= self.res.vn1_vm1_fixture
        vn1_vm2_fixture= self.res.vn1_vm2_fixture
        vm1_name= self.res.vn1_vm1_name
        vm2_name= self.res.vn1_vm2_name
        vn1_name= self.res.vn1_name
        vn1_subnets= self.res.vn1_subnets
        assert vn1_fixture.verify_on_setup()
        assert vn2_fixture.verify_on_setup()
        assert vn1_vm1_fixture.verify_on_setup()
        assert vn1_vm2_fixture.verify_on_setup()
        vm1_ipv6=vn1_vm1_fixture.get_vm_ipv6_addr_from_vm()
        vm2_ipv6=vn1_vm2_fixture.get_vm_ipv6_addr_from_vm()
        self.logger.info('Checking the communication between 2 VM using ping6 to VM link local address from other VM')
        assert vn1_vm1_fixture.ping_to_ipv6(vm2_ipv6.split("/")[0],return_output=True)
        self.logger.info('Will restart compute  services now')
        for compute_ip in self.inputs.compute_ips:
            self.inputs.restart_service('contrail-vrouter',[compute_ip])
        sleep(10)
        self.logger.info('Verifying L2 route and other VM verification after restart')
        assert vn1_vm1_fixture.verify_on_setup()
        assert vn1_vm2_fixture.verify_on_setup()
        vm1_ipv6=vn1_vm1_fixture.get_vm_ipv6_addr_from_vm()
        vm2_ipv6=vn1_vm2_fixture.get_vm_ipv6_addr_from_vm()
        self.logger.info('Checking the communication between 2 VM after vrouter restart')
        assert vn1_vm1_fixture.ping_to_ipv6(vm2_ipv6.split("/")[0],return_output=True)
        return True
    # End test_epvn_with_agent_restart
