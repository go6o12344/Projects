#include <bits/stdc++.h>

using namespace std;
char* copy(char* dest, string src){
	dest = (char*) calloc(1,src.length()+1);
	for(int i = 0;src.length();i++){
		dest[i]=src.at(0);
		src.erase(src.begin());
	}
	return dest;
}
vector<string> split_string(string input_string);
string remove_quote(string str){
	auto it = str.begin();
	for(;it!=str.end();it++){
		if((*it)=='\"')str.erase(it);
	}
	return str;
}
struct route_info{
	string address;
	int connection_index;
	int packages_sent = 0;
	route_info(string address, int connection_index){
		this->address = address;
		this->connection_index = connection_index;
	}
};
bool more_packages(route_info* a, route_info* b){
	return a->packages_sent>b->packages_sent; //promenqsh ako bugi sorta
}
int get_all_sent_count(list<route_info*> i){
	int r = 0;
	auto it = i.begin();
	for(;it!=i.end();it++){
		r=r+(*it)->packages_sent;
	}
	return r;
}
int in (list<route_info*> routes, string address){
	for(auto it = routes.begin();it!=routes.end();it++){
		if(not (*it)->address.compare(address))return distance(routes.begin(),it);
	}
	return -1;
}
class Package{
public:
	char* content;
	int content_length;
	string sender;
	string receiver;
	static int counter ;
	int package_number;
	int validate(){
		return strlen(content)==content_length ? 1 : 0;
	}
	Package(char* content, string sender, string receiver){
		if(strlen(content)==0)throw "Empty content";
		if(not sender.compare("0.0.0.0") or not sender.compare("127.0.0.0") or not receiver.compare("0.0.0.0") or not receiver.compare("127.0.0.0"))throw "Invalid IP";
		counter++;
		this->content = content;
		this->sender = sender;
		this->receiver = receiver;
		this->content_length = strlen(content);
		this->package_number = counter;
	}
	~Package(){
		free(content);
	}
};
int Package::counter = 0;
class Router{
public:
	string name;
	string address;
	vector<Router*> connections;
	list<route_info*> routing_table;
	static const int routes_max;
	static const int hops_max;
	Router(string name, string address){
		this->name = name;
		this->address = address;
	}
	void add_router(Router& router){
		if(not router.address.compare("0.0.0.0") or not router.address.compare("127.0.0.0")) throw "Invalid IP";
		connections.push_back(&router);
	}
	int query_route(const string address, const int hop_count){
		if(address==this->address)return 1;
		if(hop_count==0)return 0;
		if(in(this->routing_table,address)+1)return 1;
		for(auto it = this->connections.begin();it!=this->connections.end();it++){
			if((*it)->query_route(address, hop_count-1)){
				if(this->routing_table.size()==routes_max)this->routing_table.pop_back();
				this->routing_table.push_back(new route_info(address,it-this->connections.begin()));
				return 1;
			}
		}
		return 0;
	}
	void send_package(const Package& package){
		if(get_all_sent_count(this->routing_table)!=0 and not get_all_sent_count(this->routing_table)%10){
					printf("Sorting routing table.\n");
					this->routing_table.sort(more_packages);
					printf("Sorting successful.\n");
		}
		if(not strcmp(package.content,"")) throw "No content";
		if(package.receiver == "0.0.0.0" or package.receiver == "127.0.0.0") throw "Invalid IP";
		if(package.receiver.compare(this->address)){
			if(in(this->routing_table, package.receiver)+1){
				auto it = this->routing_table.begin();
				advance(it,in(this->routing_table,package.receiver));
				printf("Route found in routing list. Sending package to %s.\n", this->connections.at((*it)->connection_index)->address.c_str());
				//printf("Package sent successfully.\n");
				this->connections.at((*it)->connection_index)->send_package(package);
				(*it)->packages_sent++;
				return;
			}
			printf("Route not in routing list. Searching for new route.\n");
			printf("Querying route.\n");
			if(query_route(package.receiver, hops_max)){
				auto it = this->routing_table.begin();
				advance(it,in(this->routing_table,package.receiver));
				printf("Route found. Sending package to %s.\n", this->connections.at((*it)->connection_index)->address.c_str());
				printf("Package sent successfully.\n");
				this->connections.at((*it)->connection_index)->send_package(package);
				(*it)->packages_sent++;
				return;
			}
			printf("Route not found.\n");
			delete &package;
			return;
			
		}
		printf("package received successfully.\n");
	}
};
const int Router::routes_max = 10;
const int Router::hops_max = 15;
main(){
	string input;
	vector<string> split_line;
	map<string,Router*> routers_all;
	ifstream in("routers.txt");
	if(in.is_open()){
		while(not in.eof()){
			getline(in,input);
			split_line = split_string(input);
			cout << split_line.at(0) << " " << split_line.at(1) << endl;
			routers_all.insert(pair<string, Router*>(split_line.at(1),new Router(split_line.at(0), split_line.at(1))));
		}
	}
	in.close();
	in.open("network.txt");
	if(in.is_open()){
		while(not in.eof()){
			getline(in,input);
			split_line = split_string(input);
			routers_all.at(split_line.at(0))->add_router(*routers_all.at(split_line.at(1)));
			routers_all.at(split_line.at(1))->add_router(*routers_all.at(split_line.at(0)));
		}
	}
	in.close();
	in.open("packages.txt");
	if(in.is_open()){
		while(not in.eof()){
			char* content;
			getline(in,input);
			split_line = split_string(input);
			copy(content, split_line.at(2));
			split_line.at(2) = remove_quote(split_line.at(2));
			try{
				routers_all.at(split_line.at(0))->send_package(*new Package(content, split_line.at(0), split_line.at(1)));
			}
			catch(string s){
				cout << s << endl;
			}
			
		}
	}
	in.close();
	return 0;
}
vector<string> split_string(string input_string) {
    string::iterator new_end = unique(input_string.begin(), input_string.end(), [] (const char &x, const char &y) {
        return x == y and x == ' ';
    });

    input_string.erase(new_end, input_string.end());

    while (input_string[input_string.length() - 1] == ' ') {
        input_string.pop_back();
    }

    vector<string> splits;
    char delimiter = ' ';

    size_t i = 0;
    size_t pos = input_string.find(delimiter);

    while (pos != string::npos) {
        splits.push_back(input_string.substr(i, pos - i));

        i = pos + 1;
        pos = input_string.find(delimiter, i);
    }

    splits.push_back(input_string.substr(i, min(pos, input_string.length()) - i + 1));

    return splits;
}
