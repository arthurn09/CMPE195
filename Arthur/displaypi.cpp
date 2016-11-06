//============================================================================
// Name        : CMPE.cpp
// Author      :
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <pthread.h>
#include <stdlib.h>
#include <semaphore.h>
#include <fstream>
#include <string>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string>
using namespace std;

#define NO_BLIND_SPOT_CHECK_LOG		"no_blind_spot_check.log"
#define DISTRACTED_LOG				"distracted.log"
#define TAILGATE_LOG				"tailgate.log"
#define SPEED_LOG					"speed.log"
#define RECEIVE_DATA_TXT			"receive_data.txt"

sem_t master_signal, communication_signal, topspeed_signal;

void *display(void *ptr);
void *master(void *ptr);
void *communication(void *ptr);
void *GPS(void *ptr);
void *topSpeed(void *ptr);

int main() {
    
    string no_blind_spot_check_log = NO_BLIND_SPOT_CHECK_LOG; //No blindspot check file
    string distracted_log = DISTRACTED_LOG; //Distacted file
    string tailgate_log = TAILGATE_LOG; //Distance of car in front
    string speed_log = SPEED_LOG; //Speed file
    string receive_data_txt = RECEIVE_DATA_TXT; //Communication file
    
    pthread_t display_thread, master_thread, communication_thread, GPS_thead;
    
    //Four threads: display, master, communication, GPS
    pthread_create(&display_thread, NULL, display, NULL);
    pthread_create(&master_thread, NULL, master, NULL);
    pthread_create(&communication_thread, NULL, communication, NULL);
    pthread_create(&GPS_thead, NULL, GPS, NULL);
    
    
    while(1)
    {
        //Keeps program running
    }
    return 0;
}


void *display(void *ptr)
{
    while(1)
    {
        int systemCmd;
        systemCmd = system("python display.py");
        
    }
}

void *master(void *ptr)
{
    while(1)
    {
        
        //Copy contents of receive_data.log and append to data.txt
        char a[1];
        FILE *fp1;
        
        fp1 = fopen("receive_data.log", "r");
        int fd = open("data.txt", O_WRONLY | O_NONBLOCK | O_APPEND);
        
        a[0] = fgetc(fp1);
        while (a[0] != EOF)
        {
            write(fd, a, sizeof(a));
            a[0] = fgetc(fp1);
        }
        
        close(fd);
        fclose(fp1);
        
        //set semaphore for driver camera
        sem_post(&communication_signal);
        
        //wait until receiving semaphore from dashboard camera
        sem_wait(&master_signal);
    }
}

void *communication(void *ptr)
{
    while(1)
    {
        //wait for communication signal
        sem_wait(&communication_signal);
        
        int systemCmd;
        systemCmd = system("python transferReceive.py");
        
        //send master signal
        sem_post(&topspeed_signal);
    }
    
}

void *GPS(void *ptr)
{
    while(1)
    {
        int systemCmd;
        systemCmd = system("python GPS.py");
    }
    
}

void *topSpeed(void *ptr)
{
    //wait for top speed signal
    sem_wait(&topspeed_signal);
    
    static int topSpeed;
    char buffer[5];
    string speed;
    
    int fd = open("speed.txt", O_RDONLY | O_NONBLOCK);
    read(fd, buffer, 5);
    close(fd);
    for(int i = 0; i < 5; i++)
    {
        if(buffer[i] >= 48 && buffer[i] <= 57)
        {
            speed = speed + buffer[i];
        }
    }
    if(topSpeed < stoi(speed))
    {
        topSpeed = stoi(speed);
    }
    
    int fd2 = open("topspeed.txt", O_WRONLY | O_NONBLOCK);
    strcpy(buffer, speed.c_str());
    write(fd2, buffer, 5);
    close(fd2);
    
    //send master signal
    sem_post(&master_signal);
    
}

