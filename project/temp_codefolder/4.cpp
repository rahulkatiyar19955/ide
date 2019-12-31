#include<bits/stdc++.h>
using namespace std;

int convert_alpha_to_int(char s)
{
	return int(s-'a');
}
int convert_int_to_alpha(int n)
{

	char ch = 'a';
	return ch+n;
}

void display(vector<char> a)
{
	for(int i=0;i<a.size();i++)
	{
		cout<<a[i];
	}
//	cout<<endl;
}

int main()
{
	string plain;
	int key=0;
//	cout<<"kk";
//	cout<<convert_alpha_to_int(' ')<<endl;
//	cout<<char(convert_int_to_alpha(5));
//	string cipher[21];
	vector<char> ci;
	vector<char> pi;
	
//	cout<<"plain Text: ";//<<plain<<endl;
//	cin>>plain;
	getline(cin,plain);
//	cout<<"key: ";
//	key=100;
	cin>>key;
	
	for(int i=0;i<plain.length();i++)
	{
		int temp;
		if(plain[i]==' ')
		{
			ci.push_back(' ');
//			cout<<' ';
		}//sd
		else
		{
			char temp_char = plain[i];
//			temp_char.toLowerCase(temp_char);
			temp=(convert_alpha_to_int(temp_char)+key)%26;
//			cout<<char(convert_int_to_alpha(temp));
			ci.push_back(char(convert_int_to_alpha(temp)));
//			cipher[i]=char(convert_int_to_alpha(temp));
		}
		
	}
//	cout<<endl;
//	cout<<"cipherText: ";//<<cipher)<<endl;
	display(ci);
//	for(int k=0;k<26;k++)
//	{
//		for(int i=0;i<ci.size();i++)
//		{
//			int temp;
//			if(ci[i]==' ')
//			{
//				pi.push_back(' ');
//			}
//			else
//			{
//				temp=(convert_alpha_to_int(ci[i])-k)%26;
//				if(temp<0)
//				temp+=26;
//				pi.push_back(char(convert_int_to_alpha(temp)));
//			}		
//		}
//		cout<<"recovere "<<k<<": ";//<<cipher)<<endl;
//		display(pi);
//		pi.clear();
//	}
	return 0;
}
