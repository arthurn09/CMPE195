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

#define BLIND_SPOT_LOG		"blind_spot.log"
#define LANE_CHANGE_LOG		"lane_change.log"
#define DISTRACTED_LOG		"distracted.log"
#define TAILGATE_LOG		"tailgate.log"
#define SEND_DATA_LOG		"send_data.log"


sem_t master_signal, driver_signal, dashboard_signal, communication_signal;

void *driver(void *ptr);
void *dashboard(void *ptr);
void *master(void *ptr);
void *communication(void *ptr);

int main() {
    
    string blind_spot_log = BLIND_SPOT_LOG; //Blind spot check file
    string lane_change_log = LANE_CHANGE_LOG; //Lane change file
    string distracted_log = DISTRACTED_LOG; //Distracted file
    string tailgate_log = TAILGATE_LOG; //License distance file
    string send_data_log = SEND_DATA_LOG; //Communication file
    
    pthread_t driver_thread, dashboard_thread, master_thread, communication_thread;
    
    //Four threads: driver camera, dashboard camera, master, communication
    pthread_create(&driver_thread, NULL, driver, NULL);
    pthread_create(&dashboard_thread, NULL, dashboard, NULL);
    pthread_create(&master_thread, NULL, master, NULL);
    pthread_create(&communication_thread, NULL, communication, NULL);
    
    while(1)
    {
        //Keeps program running
    }
    return 0;
}

void *driver(void *ptr)
{
    while(1)
    {
        sem_wait(&driver_signal);
        
        int systemCmd;
        systemCmd = system("python driver_camera.py");
        
        sem_post(&dashboard_signal);
    }
}

void *dashboard(void *ptr)
{
    while(1)
    {
        sem_wait(&dashboard_signal);
        
        int systemCmd;
        systemCmd = system("python dashboard_camera.py");
        
        sem_post(&master_signal);
    }
}

void *master(void *ptr)
{
    ifstream distractedStream, blindspotStream, lanechangeStream, tailgatingStream;
    ofstream blindspotWrite, lanechangeWrite, distractedWrite, tailgateWrite, dataWrite;
    
    string buffer;
    bool checkedBlindspot = false;
    bool laneChange = false;
    int distractedCount = 0;
    int blindspotCount = 0;
    
    while(1)
    {
        //check distracted driving log
        distractedStream.open("distracted.log");
        while(getline(distractedStream, buffer))
        {
            //error checking for distracted driver
            if(buffer.find("distracted") != string::npos)
            {
                distractedCount = distractedCount + 2;
            }
        }
        distractedStream.close();
        
        //distracted driving detected
        if(distractedCount > 3)
        {
            //write distracted to data file
            int systemCmd;
            systemCmd = system("python DistractedDriver.py");
            
            //reset count, no need
            distractedCount = 0;
        }
        
        //check blindspot check log
        blindspotStream.open("blindspot.log");
        while(getline(blindspotStream, buffer))
        {
            //error checking for blind spot check
            if(buffer.find("blind spot") != string::npos)
            {
                blindspotCount = blindspotCount + 2;
            }
        }
        blindspotStream.close();
        
        //driver checked blind spot
        if(blindspotCount > 3)
        {
            checkedBlindspot = true;
            blindspotCount = 0;
        }
        
        //check lane change log
        lanechangeStream.open("lanechange.log");
        while(getline(lanechangeStream, buffer))
        {
            if(buffer.find("lane change") != string::npos)
            {
                //driver changed lanes
                laneChange = true;
            }
        }
        lanechangeStream.close();
        
        if(laneChange && checkedBlindspot)
        {
            //reset, no need
            laneChange = false;
            checkedBlindspot = false;
            
            //check times python script
            int systemCmd;
            systemCmd = system("python BlindSpotChangeLanes.py");
            
        }
        
        else if(laneChange && !checkedBlindspot)
        {
            //script to get time and report lane change
            
            
            //reset
            laneChange = false;
        }
        
        //check tailgating log
        tailgatingStream.open("tailgating.log");
        while(getline(tailgatingStream, buffer))
        {
            
        }
        tailgatingStream.close();
        
        
        //reset files
        blindspotWrite.open("blinspot.log");
        blindspotWrite.close();
        
        lanechangeWrite.open("lanechange.log");
        lanechangeWrite.close();
        
        distractedWrite.open("distracted.log");
        distractedWrite.close();
        
        tailgateWrite.open("tailgate.log");
        tailgateWrite.close();
        
        //set semaphore for communication camera
        sem_post(&communication_signal);
        
        //wait until receiving semaphore from dashboard camera
        sem_wait(&master_signal);
    }
}

void *communication(void *ptr)
{
    while(1)
    {
        //wait until receiving semaphore from master
        sem_wait(&communication_signal);
        
        int systemCmd;
        systemCmd = system("python transferSend.py");
        
        //set semaphore for driver camera
        sem_post(&driver_signal);
    }
    
}

