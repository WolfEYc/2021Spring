//Christian Schuering - Assignment 1
//PSID 1932884

//Program evaluates job queues and implements a FIFO basis of a waiting list for jobs

#include <iostream>
#include <string>
#include <queue>
#include <vector>
#include <numeric>

using namespace std;

void core_request(int how_long, int jobID, vector<int>& Cqueue, int &current_time, bool &core, int& core_use)
{

    if(core == true) //true == free
    {
        core = false; //false == busy
        //schedule CORE completion at time
        Cqueue.push_back(1);
        cout << "-- Job " << jobID << " requests a core at time " << current_time << " ms for " << how_long << " ms." << endl;
        current_time = current_time + how_long;
        core_use += how_long;
    }
} //core_request

//change to int to return completion time?
bool core_release(int how_long, int jobID, vector<int>& Cqueue, int &current_time, bool &core)
{
    if(!Cqueue.empty())
    {
        Cqueue.pop_back();
        //current_time = current_time + how_long; //how_long == jobID
        core = true;
        cout << "-- Job " << jobID << " will release a core at time " << current_time << " ms." << endl;
        return true;
    }
    //process next job request for job jobID
} //core_release

void disk_request(int how_long, int jobID, vector<int>& Dqueue, int &current_time, bool &disk)
{
    if(disk == true) //true == free
    {
        disk = false; //false == busy
        //schedule DISK completion event at time
        Dqueue.push_back(1);
        cout << "-- Job " << jobID << " requests disk access at time " << current_time << " ms for " << how_long << " ms." << endl;
        current_time = current_time + how_long;
    }
} // disk_request

bool disk_release(int how_long, int jobID, vector<int>& Dqueue, int &current_time, bool &disk)
{
    if(!Dqueue.empty())
    {
        Dqueue.pop_back();
        //current_time = current_time + how_long; //how_long == jobID
        disk = true;
        cout << "-- Job " << jobID << " will release the disk at time " << current_time << " ms." << endl;
        return true;
    }
    //process next job request for job jobID
} //disk_release

void spooler_request(int how_long, int jobID, vector<int>& Squeue, int &current_time, bool &spooler)
{
    if(spooler == true) //true == free //should be spooler bool?
    {
        spooler = false;
        //schedule SPOOLER completion event at time
        Squeue.push_back(1);
        cout << "-- Job " << jobID << " requests spooler access at time " << current_time << " ms for " << how_long << " ms." << endl;
        current_time = current_time + how_long;
    }
} //spooler_request

bool spooler_release(int how_long, int jobID, vector<int>& Squeue, int &current_time, bool &spooler)
{
    if(!Squeue.empty())
    {
        Squeue.pop_back();
        //current_time = current_time + how_long;
        spooler = true;
        cout << "-- Job " << jobID << " will release the spooler at time " << current_time << " ms." << endl;
        return true;
    }
    //process next job request for job jobID
} //spooler_release

void print(int completedtime, int i, bool& core, bool& disk, bool& spooler, bool& terminate) //i poses as the job number
{
    cout << endl;
    cout << "Job " << i << " terminates at time " << completedtime << " ms." << endl;
    cout << "Job Table:" << endl;
    if(core == false && disk == false && spooler == false) //must find out how to see if job is completed or not for function.
    {
        cout << "Job " << i << " is RUNNING" << endl;
    }
    else if(terminate == true)
    {
        cout << "Job " << i << " is TERMINATED." << endl;
    }
    else //if job is completed
    {
        cout << "There are no active jobs" << endl;
    }
    terminate = false;
}

int maxRowLength(vector<vector<pair<string,int>>> v){
    vector<int> temp;
    for(auto i:v)
        temp.push_back(i.size());
    
    int max = 0;
    for(int i:temp)
        if(max<i)
            max=i;
    return max;
}

bool procDone(vector<vector<pair<string,int>>> v, vector<int> rowIt,int row){
    return rowIt[row]>=v[row].size();
}

int main()
{
    //head node is the 0th node when starting
    //node* head;

    //linecounter = jobstarting number && linecounter = jobending number
    //linecounter* head;

    vector<vector<pair<string,int>>> processes;

    vector<int> currentIterationofeachrow(processes.size());

    //vector<string> veckeyword; //keyword
    //vector<int> vecargument; //argument
    //vector<int> jobnumber; //iterates anytime a new job is issued
    //vector<int> expectedtimeforjob; //pushes expected time for each new job

    //vector holders to find if we have something in the core or not
    vector<int> Disk_queue;
    vector<int> Spooler_queue;
    vector<int> Core_queue;

    //array holds core, disk and spooler;
    string keyword;
    string argument;

    //bools if theyre ready or not
    bool disk = true; //true means ready //false means busy
    bool core = true; //true means ready //false means busy
    bool spooler = true; //true means ready //false means busy
    bool terminate = false; //true means a job is terminating

    //counter for expected time finish
    int time_taken = 0;
    int time_taken_for_all = 0;

    //holds job number
    int jobID = 1; //always start at job # 1
    int jobcounter = 1;

    //count for all disks and cores added
    int diskcounter = 0;
    int corecounter = 0;
    int core_use = 0;

    int MPL;
    string gaybitch;
    cin>>gaybitch>>MPL;
    cout << MPL;
    while(cin >> keyword >> argument)
    {
        pair<string,int> addthis(keyword,stoi(argument));
        //cout << keyword << argument << endl;
        //addnode(head, keyword, argument);
        //veckeyword.push_back(keyword);
        //int hold = stoi(argument);
        //vecargument.push_back(stoi(argument));

        if(keyword == "JOB"){
            vector<pair<string,int>> newjob;
            newjob.push_back(addthis);
            processes.push_back(newjob);
        }else{
            processes[processes.size()-1].push_back(addthis);
        }
    }
    int bscounter = 0;
    cout << "/////////////////////////////////////" << endl;

    int maxLength = maxRowLength(processes);

while(69==69){
    for(int keyword_iteration = jobcounter; keyword_iteration < jobcounter+MPL && jobcounter+MPL<=processes.size(); keyword_iteration++) //keyword_iteration == i
    {
        //equation start
        //cout << veckeyword[keyword_iteration] + " ";
        //cout << vecargument[keyword_iteration];
        //cout << endl;
        //this works^

        if(procDone(processes,currentIterationofeachrow,keyword_iteration)){//this job es done
            jobcounter++;
            
        }

        string processName = processes[keyword_iteration][currentIterationofeachrow[keyword_iteration]].first;
        int number = processes[keyword_iteration][currentIterationofeachrow[keyword_iteration]].second;


        if(processName == "PRINT")
        {
            spooler_request(number, jobID, Spooler_queue, time_taken, spooler);
        }
        else if(processName == "CORE")
        {
            corecounter++;
            core_request(number, jobID, Core_queue, time_taken, core, core_use);
        }
        else if(processName == "DISK")
        {
            diskcounter++;
            disk_request(number, jobID, Disk_queue, time_taken, disk);
        }
        else if(processName == "JOB") //takes in the job #
        {

            jobID = vecargument[keyword_iteration];
            //jobnumber.push_back(vecargument[keyword_iteration]);

            cout << endl << endl;
            cout << "Job " << jobID << " is fetched at time " << time_taken << " ms" << endl;
            cout << "Job Table: " << endl;
            cout << "There are no active jobs. " << endl << endl;

            /*int time_complexity_iteration = keyword_iteration;
            while(veckeyword[time_complexity_iteration] != "JOB") // then iterates through the keywords, while at the same time ignoring the keyword JOB
            {
                time_taken_for_all += (vecargument[time_complexity_iteration]); //adding the arguments up until the next job
                //cout << time_taken_for_all << " ";
                time_complexity_iteration++;
                if(veckeyword[time_complexity_iteration] == "JOB")
                {
                    cout << time_taken_for_all << " ";
                    expectedtimeforjob.push_back(time_taken_for_all); //giving an expected time completion for each new job
                }
            }*/
        }

        if (spooler_release(vecargument[keyword_iteration], jobID, Spooler_queue, time_taken, spooler) == false); //must set to be true
        if (core_release(vecargument[keyword_iteration], jobID, Core_queue, time_taken, core) == false); //must set to be true
        if (disk_release(vecargument[keyword_iteration], jobID, Disk_queue, time_taken, disk) == false); //must set to be true
        //for all 3 of these, implenet a jobqueue that pops when the releases are called, and pushed when the requests are called
        //cout << bscounter++ << endl; //loops through 148 times for input10.txt
    }
}
    
    cout << endl;

    float coresadded = 0;

    cout << "SUMMARY:" << endl;
    cout << "Totaly elapsed time: " << time_taken << " ms" << endl;
    cout << "Number of jobs that completed: " << jobID << endl;
    cout << "Total number of disk access: " << diskcounter << endl;
    cout << "CPU utilization: ";
    printf("%.3f",(float)(core_use)/(float)(time_taken));
    cout << endl; //add up entire elapsed time and divide core times added by the entireelapsed time
                                    //maybe just use (float coresadded = coreutilization/expectedtimeforjob[i];)

    return 0;
}
//get timer working
//3 queues
//add time each process finishes at and divide it by number of jobs = computing itme;
//total simulation time in ms - 
//number of jobs that have been completed - 
//total number of disc requests - 
//cpu utilization, fraction of time device was busy between 0 and 1 -
//must use strings, manipulate when changing to ints then change back to strings for final output
//have multiple vectors, possibly use priority queue, sort vectors with multiple copies of jobs depending on the MPL size
//say we have an MPL 3, have vectors with every job and sort them using for loops