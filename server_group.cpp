#include <unistd.h>
#include "includes.h"
#include "server.h"
#include "BBB_I2C.h"
#include "MPU6050.h"

int n=0;

server::server(int Port){
	port = Port;
	bzero((char *) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(port);
}

server::~server(){
	close(newsockfd);
	close(sockfd);
}

bool server::_acceptCon(){
    clilen = sizeof(cli_addr);
	newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
     if (newsockfd < 0){
          error("ERROR on accept connection");
          return 0;
    }
	return 1;
};

char* server::_readSock(){
	bzero(buffer,256);
	sockReturn = read(newsockfd,buffer,255);
	if (sockReturn < 0){
		error("ERROR reading from socket");
		return NULL;
	}
	return buffer;
};	

bool server::_writeSock(char* msg){
	sockReturn = write(newsockfd,msg,1024);
	if (sockReturn < 0){
		error("ERROR writing to socket");
		return 0;
	}
	return 1;
}

/*
void server::_conHandler(int sock){
	int n;
	char buffer[256];
	char msg[32] = {"I've got your message\n\0"};
	printf("message: %s\n",_readSock());
	_writeSock(msg);
}
*/
void server::_conHandler(int sock){
	struct timespec start, end, timepcs;
	int16_t ax,ay,az;
	int16_t gx,gy,gz;
	char buffer[256];
	char msg_pcs[64] = {};
	char msg[1024] ={};
	//printf("Rx message: %s\n",_readSock());
	
	MPU6050 MPU;
	BBB_I2C BBB_I2C;
	
	if (MPU.testConnection() < 1){
		printf ("Device ID not match!\n");
		exit(1);
	}
	
	if (MPU.initialize() < 1) {
		printf ("MPU initialize fail!\n");
		exit(1);
	}
	
	clock_gettime( CLOCK_REALTIME, &start );	//must linked with the "librt" library to use these functions
	
while(1){
	n++;
	
	sprintf(msg,"");
	
//	clock_gettime( CLOCK_REALTIME, &start );	//must linked with the "librt" library to use these functions
	
//	if (freopen("mpu6050_output.csv", "w", stdout)==NULL)
//		fprintf(stderr, "data redirecting stdout\n");

//read 500 times write to file
	for(int i=0;i<20;i++){
		MPU.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
 	    clock_gettime( CLOCK_REALTIME, &timepcs );
		double difference = (timepcs.tv_sec - start.tv_sec) + (double)(timepcs.tv_nsec - start.tv_nsec)/1000000000.0d;
//		fprintf (stdout,"%f,", difference);
//		fprintf (stdout,"%d,%d,%d,%d,%d,%d\n",ax,ay,az,gx,gy,gz);

		sprintf (msg_pcs,"%f,%d,%d,%d,%d,%d,%d\n",difference,ax,ay,az,gx,gy,gz);
		strcat (msg,msg_pcs);
		usleep(20000);
	}
	
	_writeSock(msg);


//	fclose(stdout);
	
	fprintf(stderr, "Tx [%d] Done. \n",n);
}
	fprintf(stderr,"Data transfer done.\n");
	//_writeSock(msg);

}

bool server::_fork(){
	pid = fork();
	if (pid < 0){
		error("ERROR on fork");
		return 0;
	}
	if (pid == 0){
		close(sockfd);
		_conHandler(newsockfd);
		close(newsockfd);
		exit(0);
	}
	else close(newsockfd);
	return 1;
}

bool server::openSocket(){
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0){
	    error("ERROR opening socket");
	    return 0;
	}
	else return 1;
}

bool server::bindAndListen(){
	char msg[32] = {"I've got your message\n\0"};
	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0){
		error("ERROR on binding");
		return 0;
	}
	
	listen(sockfd,5);
	while(true){
		_acceptCon();
		_fork();
	}

	return 1;
}
