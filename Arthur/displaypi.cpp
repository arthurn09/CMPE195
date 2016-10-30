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
using namespace std;

#define NO_BLIND_SPOT_CHECK_LOG		"no_blind_spot_check.log"
#define DISTRACTED_LOG				"distracted.log"
#define TAILGATE_LOG				"tailgate.log"
#define SPEED_LOG					"speed.log"
#define DATA_LOG					"data.log"

sem_t master_signal, communication_signal, GPS_signal, display_signal;

void *display(void *ptr);
void *master(void *ptr);
void *communication(void *ptr);
void *GPS(void *ptr);

int main() {
    
    string no_blind_spot_check_log = NO_BLIND_SPOT_CHECK_LOG; //No blindspot check file
    string distracted_log = DISTRACTED_LOG; //Distacted file
    string tailgate_log = TAILGATE_LOG; //Distance of car in front
    string speed_log = SPEED_LOG; //Speed file
    string data_log = DATA_LOG; //Communication file
    
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
        //Might not need since display runs on another program
        //wait for display signal
        sem_wait(&display_signal);
        
        int systemCmd;
        systemCmd = system("python display.py");
        
        //send communication signal
        sem_post(&communication_signal);
    }
}

void *master(void *ptr)
{
    while(1)
    {
        
        //Determine grade
        ifstream dataStream;
        string buffer;
        dataStream.open("data.log");
        while(getline(dataStream, buffer))
        {
            
        }
        
        
        //set semaphore for driver camera
        sem_post(&display_signal);
        
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
        systemCmd = system("python communicaiton.py");
        
        //send GPS signal
        sem_post(&GPS_signal);
    }
    
}

void *GPS(void *ptr)
{
    while(1)
    {
        //wait for GPS signal
        sem_wait(&GPS_signal);
        
        int systemCmd;
        systemCmd = system("python GPS.py");
        
        //send master signal
        sem_post(&master_signal);
    }
    
}
