#include <iostream>
#include <string>
#include <vector>

using namespace std;
enum SportNumber{
    PlayersSize = 10,
    Coaches = PlayersSize,
    Rules = 4,
};

class Sport {
    public: 
        // vector<string> Players;
        // string Players**;Thanks
        string Players[10];
        string Coaches[10];
        string Rules [4];
        int score = 0;
        virtual void AddScore() = 0;
        virtual void Run() = 0;
        virtual void Stop() = 0; 
};

class Baseball: public Sport {
    public:
        
        void AddScore()
        {
            cout<<"Homerun"<<endl;
        }
        void Run()
        {
            cout<<"Coyeye"<<endl;
        }
        void Stop()
        {
            cout<<"Safe"<<endl;
        }
};
class Football: public Sport{ // Americano?
    public:
        void AddScore()
        {
            cout<<"TouchDown:6pts"<<endl;
        }
        void Run()
        {
            cout<<"15 yds Rush"<<endl;
        }
        void Stop()
        {
            cout<<"Ball at 20 yard line"<<endl;
        }
};

void Game(Sport* sport)
{
    sport->Run();
    sport->AddScore();
    sport->Stop();
}

int main(int argc, char const *argv[])
{
    /* code */
    //Football footbal();?
    Sport* footBall = new Football();
    Sport* baseBall = new Baseball();
    
    Game(footBall);
    Game(baseBall);
    
    delete footBall;
    delete baseBall;
    return 0;
} 

// Pónganos 10 profe NEIN
