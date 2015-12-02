#include <iostream>
#include <vector>

#include <math.h>

class Rules{
public:
  int playerNr;
  Rules(int);
  Rules returnCopy();
  std::vector<int> returnAllLegalMoves(std::vector<int>);
};

Rules::Rules(int playerNrIn){
  playerNr = playerNrIn;
};

Rules Rules::returnCopy(){
  Rules newRules(playerNr);
  return newRules;
};

std::vector<int> Rules::returnAllLegalMoves(std::vector<int> field){
  std::vector<int> newVec;
  newVec.assign(2,3);
  return newVec;
};

class MonteNode{
  int playerNr, wins, draws, losses, moveNr;
  std::vector<int> field;
  MonteNode* parent;
  std::vector<MonteNode*> children;
  Rules *rules;
  bool leaf;
  float c;

  void backPropagation(int);

public:
  MonteNode(MonteNode*, std::vector<int>, int, float, int, Rules*);
  int pickExploreNode(int);
};

MonteNode::MonteNode(MonteNode* parentIn, std::vector<int> fieldIn, int playerNrIn, float cIn, int moveNrIn, Rules* rulesPtr){

  parent = parentIn;
  playerNr = playerNrIn;
  field.assign(fieldIn.begin(), fieldIn.end());
  wins = 0;
  losses = 0;
  draws = 0;
  c = cIn;
  leaf = true;

  moveNr = moveNrIn;

  rules = rulesPtr;
  rules->playerNr = playerNr;
  children.assign((rules->returnAllLegalMoves(field)).size(),NULL);
};

int MonteNode::pickExploreNode(int nodeIndependentPlayerNr){
  int counter = 0;
  float bestVal;
  int bestIndex;
  if(nodeIndependentPlayerNr == this->playerNr){
    bestVal = -1.0f;
    bestIndex = 0;
  }
  else{
    bestVal = 1.0f;
    bestIndex = 0;
  }
  int totalSimulations = 0;
  std::vector<MonteNode*>::iterator it = this->children.begin();
  counter = 0;
  while(it != this->children.end()){
    if (*it == NULL){
      return counter;
    }
    totalSimulations += (*it)->wins+(*it)->draws+(*it)->losses;
    it++;
    counter++;
  }
  float totalSimulationsF = float(totalSimulations);
  counter = 0;
  it = this->children.begin();
  int n;
  while (it!=this->children.end()) {
    n = (*it)->wins+(*it)->losses+(*it)->draws;
    if (n==0) {
      return counter;
    }
    float tmp = float((*it)->wins)/n+this->c*sqrt(log(totalSimulationsF)/n);
    if((tmp >= bestVal && nodeIndependentPlayerNr==this->playerNr) || (tmp<bestVal && nodeIndependentPlayerNr != this->playerNr)){
      bestVal = tmp;
      bestIndex = counter;
    }
    counter++;
    it++;
  }
  return bestIndex;
};

void MonteNode::backPropagation(int winner){
  if(winner==1){
    this->wins++;
  }
  else if(winner == 2){
    this->losses++;
  }
  else{
    this->draws++;
  }
  if(this->parent != NULL){
    this->parent->backPropagation(winner);
  }
};

void MonteNode::explore(int nodeIndependentPlayerNr){
  if((this->children).size()==0){
    int p = this->rules->playerNr;
    int w;
    if(this->rules->isOver(this->field)){
      if(this->rules-hasWon(this->field)){
        w = p==nodeIndependentPlayerNr ? 1 : -1;
      }
      else if(this->rules->hasLost(this->field)){
        w = p==nodeIndependentPlayerNr ? -1 : 1;
      }
      else{
        w = 0;
      }
    }
    if (w==1) {
      this->backPropagation(1);
    } else if (w==-1) {
      this->backPropagation(2);
    } else {
      this->backPropagation(0);
    }
  }
  int r = this->pickExploreNode(nodeIndependentPlayerNr);
  if(this->children[r]==NULL){
    std::vector<int> newField = field;
    this->leaf = false;
    std::vector<int> moves = this->rules->returnAllLegalMoves(newField);
    newField = this->rules->makeMove(newField,moves[r], this->playerNr);

    Rules* newRules = this->rules->returnCopy();
    newRules->playerNr = this->rules->otherPlayerNr();

    this->children[r] = MonteNode(this,newField, newRules->playerNr,this->c,this->moveNr+1,newRules);
    w = this->children[r]->simulateRandomGame(nodeIndependentPlayerNr);
    if (w==1) {
      this->backPropagation(1);
    } else if (w==-1) {
      this->backPropagation(2);
    } else {
      this->backPropagation(0);
    }
  }
  else{
    this->children[r]->explore(nodeIndependentPlayerNr);
  }
};

int MonteNode::simulateRandomGame(int nodeIndependentPlayerNr){
  bool keepGoing = true;
  std::vector<int> players = this->rules->getPlayerList();

  Rules* rulesCopy = this->rules->returnCopy();
  rulesCopy->playerNr = this->playerNr;

  players = shift();//FIX!
  std::vector<int> fieldNew = this->field;

  int p;
  while (keepGoing) {
    for (size_t i = 0; i < players.size(); i++) {
      p = players[i];
      std::vector<int> moves = rulesCopy->returnAllLegalMoves(fieldNew);
      if(moves.size() != 0){
        int rand = randint(0, moves.size()); //FIX!
        fieldNew = rulesCopy->makeMove(fieldNew, moves[rand],p);
      }
      else{
        if(rulesCopy->isOver(fieldNew)){
          keepGoing = false;
          if (rulesCopy->hasWon(fieldNew)) {
            if (p==nodeIndependentPlayerNr) {
              return 1;
            } else {
              return -1;
            }
          } else if (rulesCopy->hasLost(fieldNew)) {
            if (p==nodeIndependentPlayerNr) {
              return -1;
            } else {
              return 1;
            }
          } else {
            return 0;
          }
        }
      }
      if(rulesCopy->isOver(fieldNew)){ //Isn't this and all the stuff below just repetition? And unnessecary.
        keepGoing = false;
        if (rulesCopy->hasWon(fieldNew)) {
          if (p==nodeIndependentPlayerNr) {
            return 1;
          } else {
            return -1;
          }
        } else if (rulesCopy->hasLost(fieldNew)) {
          if (p==nodeIndependentPlayerNr) {
            return -1;
          } else {
            return 1;
          }
        } else {
          return 0;
        }
      }
    }
  }

};

int main(int argc, char const *argv[]) {
  Rules r(1);
  std::vector<int> field;
  field.assign(4,5);
  MonteNode monteNode (NULL,field,1,1.414f,0,&r);
  std::cout<<"Done!"<<std::endl;
  return 0;
};
