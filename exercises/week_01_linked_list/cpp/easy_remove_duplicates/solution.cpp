// 문제 설명: problem.md

struct Node {  // 주어진 노드 타입
    int value;
    Node *next;
};

// 정렬된 values 로 리스트를 만들어 중복을 지우고 out 에 쓴다.
// 반환: 쓴 개수. out_capacity 가 모자라면 -1.
extern "C" int dedup_sorted(const int *values, int n, int *out, int out_capacity)
{
    return -1;  // TODO
}
