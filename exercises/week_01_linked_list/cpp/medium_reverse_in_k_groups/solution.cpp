// 문제 설명: problem.md

struct Node {  // 주어진 노드 타입
    int value;
    Node *next;
};

// values 로 리스트를 만들어 앞에서부터 k개씩 뒤집고 out 에 쓴다.
// 반환: 쓴 개수(= n). k < 1 이거나 out_capacity 가 모자라면 -1.
extern "C" int reverse_groups(const int *values, int n, int k, int *out, int out_capacity)
{
    return -1;  // TODO
}
