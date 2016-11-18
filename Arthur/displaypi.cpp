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

//display.py
//transferReceive.py
//GPS.py
//receive_data.log
//tailgate.log
//data.txt
//speed.txt
//topspeed.txt
//speed.txt

sem_t master_signal, communication_signal, topspeed_signal, tailgate_signal;

void *display(void *ptr);
void *master(void *ptr);
void *communication(void *ptr);
void *GPS(void *ptr);
void *topSpeed(void *ptr);
void *tailgate(void *ptr);

int main() {
    
    
    pthread_t display_thread, master_thread, communication_thread, GPS_thead, topSpeed_thread, tailgate_thread;
    
    //Four threads: display, master, communication, GPS
    pthread_create(&display_thread, NULL, display, NULL);
    pthread_create(&master_thread, NULL, master, NULL);
    pthread_create(&communication_thread, NULL, communication, NULL);
    pthread_create(&GPS_thead, NULL, GPS, NULL);
    pthread_create(&topSpeed_thread, NULL, topSpeed, NULL);
    pthread_create(&tailgate_thread, NULL, tailgate, NULL);
    
    
    
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
        char a[50];
        
        //exclusive lock for receive_data
        struct flock fl1 = {F_UNLCK, SEEK_SET, 0, 100, 0};
        struct flock fl2 = {F_UNLCK, SEEK_SET, 0, 100, 0};
        
        fl1.l_type = LOCK_EX;
        fl2.l_type = LOCK_EX;
        
        int fd1 = open("receive_data.log", O_RDONLY);
        fcntl(fd1, F_SETLKW,&fl1);
        
        int fd2 = open("data.txt", O_WRONLY | O_APPEND);
        fcntl(fd2, F_SETLKW,&fl2);
        
        ofstream tailgateStream;
        tailgateStream.open("tailgate.log");
        while(read(fd1, a, sizeof(a)))
        {
            if(strstr(a, "tailgate"))
            {
                tailgateStream << a;
            }
            else
            {
                write(fd2, a, sizeof(a));
            }
        }
        
        
        fl1.l_type = LOCK_UN;
        fl2.l_type = LOCK_UN;
        
        fcntl(fd1, F_SETLK,&fl1);
        fcntl(fd2, F_SETLK,&fl2);
        
        close(fd1);
        close(fd2);
        tailgateStream.close();
        
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
    while(1)
    {
        //wait for top speed signal
        sem_wait(&topspeed_signal);
        
        static int topSpeed;
        char buffer[5];
        string speed;
        
        //exclusive lock for receive_data
        struct flock fl1 = {F_UNLCK, SEEK_SET, 0, 100, 0};
        fl1.l_type = LOCK_EX;
        
        int fd = open("speed.txt", O_RDONLY);
        fcntl(fd, F_SETLKW,&fl1);
        
        read(fd, buffer, 5);
        
        fl1.l_type = LOCK_UN;
        fcntl(fd, F_SETLK,&fl1);
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
        
        //exclusive lock for receive_data
        struct flock fl2 = {F_UNLCK, SEEK_SET, 0, 100, 0};
        fl2.l_type = LOCK_EX;
        
        int fd2 = open("topspeed.txt", O_WRONLY);
        fcntl(fd2, F_SETLKW, &fl2);
        
        strcpy(buffer, speed.c_str());
        write(fd2, buffer, 5);
        
        fl2.l_type = LOCK_UN;
        fcntl(fd2, F_SETLK,&fl2);
        close(fd2);
        
        //send tailgate signal
        sem_post(&tailgate_signal);
    }
}

void *tailgate(void *ptr)
{
    while(1)
    {
        //wait for tailgate signal
        sem_wait(&tailgate_signal);
        
        ifstream tailgateStream, speedStream;
        string tailgate, speedString;
        char speed[5];
        char tailgateBuffer[50];
        
        //exclusive lock for receive_data
        struct flock fl1 = {F_UNLCK, SEEK_SET, 0, 100, 0};
        fl1.l_type = LOCK_EX;
        
        int fd = open("speed.txt", O_RDONLY);
        fcntl(fd, F_SETLKW,&fl1);
        
        read(fd, speed, 5);
        
        fl1.l_type = LOCK_UN;
        fcntl(fd, F_SETLK,&fl1);
        close(fd);
        
        //convert speed from char array to string
        for(int i = 0; i < 5; i++)
        {
            if(speed[i] >= 48 && speed[i] <= 57)
            {
                speedString = speedString + speed[i];
            }
        }
        
        //check speed greater than 50
        if(stoi(speedString) > 50)
        {
            //exclusive lock for receive_data
            struct flock fl2 = {F_UNLCK, SEEK_SET, 0, 100, 0};
            fl2.l_type = LOCK_EX;
            
            struct flock fl3 = {F_UNLCK, SEEK_SET, 0, 100, 0};
            fl3.l_type = LOCK_EX;
            
            //get tailgate
            int fd2 = open("tailgate.log", O_RDONLY);
            fcntl(fd2, F_SETLKW,&fl2);
            
            read(fd2, tailgateBuffer, sizeof(tailgate));
            
            fl2.l_type = LOCK_UN;
            fcntl(fd2, F_SETLK,&fl2);
            close(fd2);
            
            //append tailgate
            int fd3 = open("data.txt", O_WRONLY | O_APPEND);
            fcntl(fd3, F_SETLKW,&fl3);
            
            write(fd3, tailgateBuffer, sizeof(tailgate));
            
            fl3.l_type = LOCK_UN;
            fcntl(fd3, F_SETLK,&fl3);
            close(fd3);
        }
        
        //send master signal
        sem_post(&master_signal);
        
    }
}
