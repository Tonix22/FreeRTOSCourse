#include <iostream>

struct Node {
    int data;
    Node* next;

    Node(int val) : data(val), next(nullptr) {}
};

// Function to add a node at the beginning of the linked list.
void addNode(Node* head, int value) {
    Node* newNode = new Node(value);
    newNode->next = head;
    head = newNode;  // This change affects only the local copy of head.
}

// Function to print the linked list.
void printList(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " -> ";
        temp = temp->next;
    }
    std::cout << "nullptr" << std::endl;
}

int main() {
    Node* head = nullptr;

    addNode(head, 1);
    addNode(head, 2);
    addNode(head, 3);

    // Expected to print "3 -> 2 -> 1 -> nullptr"
    // Actually prints "nullptr" due to the error in addNode function.
    printList(head);

    // Cleanup to prevent memory leak
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }

    return 0;
}
