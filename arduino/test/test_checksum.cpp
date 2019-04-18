//return true of checksum passes
//Return false of checksum did not pass
#ifndef ARDUINO_H
#include <Arduino.h>
#endif
#define MAX_NUM 255
bool testChecksum(void (*f)(char*, int));

bool testChecksum(void (*f)(char*, int)){
    char data[5];
    for(int i = 0; i < MAX_NUM; i+=10)
    {
        data[0] = i;
        for(int j = 0; j < MAX_NUM; j+=10)
        {
            data[1] = j;
            for(int k = 0; k < MAX_NUM; k+=10)
            {
                data[2] = k;
                for(int l = 0; l < MAX_NUM; l+=10)
                {
                    data[3] = l;
                    (*f)(data, 4);                  //Calc check sum
                    char sum = 0;
                    for(int m = 0; m < 5; m++){     //Verify checksum
                        sum+=data[m];
                    }
                    if (sum != 0) {
                        Serial.printf("Failed, data: [%d, %d, %d, %d], checksum: %d\n", i,j,k,l,data[4]);
                        return false;
                    }
                }
            }
        }
    }
    return true;
}