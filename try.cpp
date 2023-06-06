#include <stdio.h>

int main()
{
    int number, limit, product;

    printf("Enter The Number :\n");
    scanf("%d", &number);

    printf("Enter The limit :\n");
    scanf("%d", &limit);

    int i = 0;

    while (i <= limit)
    {
        i++;
        product = number * i;
        printf("%d * %d is %d\n", number, i, product);
    }

    return 0;
}