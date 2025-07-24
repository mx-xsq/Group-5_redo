/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;               // Value of the node
 *     ListNode *next;        // Pointer to the next node in the list
 *     ListNode(int x) : val(x), next(NULL) {}  // Constructor
 * };
 */

class Solution {
public:
    /**
     * Determines whether a singly linked list has a cycle.
     *
     * @param head Pointer to the head of the linked list.
     * @return true if there is a cycle; otherwise, false.
     */
    bool hasCycle(ListNode *head) {
        // Base case: If the list is empty or has only one node, it can't have a cycle.
        if (!head || !head->next) return false;

        // Initialize two pointers:
        // - slow moves one step at a time
        // - fast moves two steps at a time
        ListNode* slow = head;
        ListNode* fast = head->next;

        // Loop until the two pointers meet or the fast pointer reaches the end
        while (slow != fast) {
            // If fast reaches the end, there's no cycle
            if (!fast || !fast->next) return false;

            // Move slow one step, fast two steps
            slow = slow->next;
            fast = fast->next->next;
        }

        // If slow and fast meet, there's a cycle
        return true;
    }
};
