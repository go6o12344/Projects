class Board{
public:	
	vector<Vector> boardEnds;
	Board(vector<pair<int,int>> v){
		this->boardEnds->push_back(v.at(0));
		this->boardEnds->push_back(v.at(1));
		this->boardEnds->push_back(v.at(2));
		this->boardEnds->push_back(v.at(3));
	}
	Board& normalize(){
		
	}
};