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
#include <string.h>
using namespace std;

//display.py
//transferReceive.py
//GPS.py

//receive_data.log
//tailgate.log
//data.txt
//topspeed.txt
//speed.txt

sem_t master_signal, communication_signal, topspeed_signal, tailgate_signal, grade_signal;

void *display(void *ptr);
void *master(void *ptr);
void *communication(void *ptr);
void *GPS(void *ptr);
void *topSpeed(void *ptr);
void *tailgate(void *ptr);
void *grade(void *ptr);


int gradeCount = 0;

int main() {
    
    
    int systemCmd;
    systemCmd = system("python display.py");
    return 0;
}



