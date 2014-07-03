#include "includes.h"
#include "server.cpp"
#include <stdio.h>
#include <iostream>
#include <string>
#include <unistd.h>
#include <time.h>
#include "BBB_I2C.h"
#include "MPU6050.h"

using namespace std;

int main(int argc, char** argv){

	cout << "Testing the MPU6050 server 00.00.01" << endl;

	if(argv[1] == NULL){
		cout<<"Ussage:\n\tserver [port]"<<endl;
		return 0;
	}
	int port = atoi(argv[1]);
	server s(port);
	s.openSocket();
	s.bindAndListen();
	
	
	return 1;
}

