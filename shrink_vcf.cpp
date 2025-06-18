#include <iostream>
#include <fstream>
#include <unordered_set>
#include <string>
#include <sstream>

using namespace std;
enum class READING_STATE { CHECK, PRINT, TERMINATE };
#define CHECK READING_STATE::CHECK
#define PRINT READING_STATE::PRINT
#define TERMINATE READING_STATE::TERMINATE

int main() {
    string CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO;
    unordered_set<string> INFO_SET = {
        "AF_afr", 
        "AF_amr",
        "AF_ami",
        "AF_asj",
        "AF_eas",
        "AF_fin",
        "AF_nfe",
        "AF_sas",
        "AF_remaining",
        "AF"
    };
    string line;
    while (getline(cin, line)) {
        if (line.empty())
            continue;
        if (line[0] == '#') {
            cout << line << endl;
            continue;
        }
        READING_STATE state = CHECK;
        string attr = "";
        stringstream ss(line);
        if (!(ss >> CHROM >> POS >> ID >> REF >> ALT >> QUAL >> FILTER >> INFO)) {
            cerr << "Error reading line: " << line << endl;
            continue;
        }
        cout << CHROM << "\t" << POS << "\t" << ID << "\t" << REF << "\t" << ALT << "\t" << QUAL << "\t" << FILTER << "\t";
        for (char &c: INFO) {
            if (state == CHECK) {
                if (c == '=') {
                    if (INFO_SET.find(attr) != INFO_SET.end()) {
                        state = PRINT;
                        cout << attr << "=";
                        attr.clear();
                    } else {
                        state = TERMINATE;
                        attr.clear();
                    }
                } else if (c == ';') {
                    attr.clear();
                } else {
                    attr += c;
                }
            } else if (state == PRINT) {
                if (c == ';') 
                    state = CHECK;
                cout << c;
            }
            else if (state == TERMINATE) {
                if (c == ';') {
                    state = CHECK;
                }
            }
            else if (c == '|')
                break;
        }
        cout << endl;
    }
    INFO_SET.clear();
    return 0;
}